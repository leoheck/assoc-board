#!/usr/bin/env python3
"""Kicad script to create a BOM according to the Seeed Studio Fusion PCBA."""

# HOW TO ADD IT IN KICAD
# python3 "$(pwd)/library/scripts/perimeter-bom.py" "%I" "%O.csv"

import argparse
import csv
import sys
import xml.etree.ElementTree as ET

from pprint import pprint

import re


def parse_command_line():
	parser = argparse.ArgumentParser(description='Generate Bill of Materials (csv) for Seeedstudio')
	parser.add_argument('input_file', metavar='XML', help='Input file .xml')
	parser.add_argument('output_file', metavar='CSV', help='Output file .csv')
	args = parser.parse_args()
	return args


def unique(list1): 
	unique_list = [] 
	for x in list1: 
		if x not in unique_list: 
			unique_list.append(x) 
	return unique_list


def parse_kicad_xml(input_file):

	"""
	Kicad XML parser.
	Parse the KiCad XML file and look for the part designators
	as done in the case of the official KiCad Open Parts Library:
	* other parts are designated with "MPN"
	"""

	comps = {}

	tree = ET.parse(input_file)
	root = tree.getroot()

	for f in root.findall('./components/'):

		name = f.attrib['ref']
		fields = f.find('fields')

		p = re.compile('MPN[0-9]')

		comps[name] = {}
		comps[name]['desc'] = None
		comps[name]['dnm'] = False
		comps[name]['mpn'] = None
		comps[name]['mpns'] = None

		mpns = []

		if fields is not None:

			for x in fields:
				if x.attrib['name'] == 'Description':
					comps[name]["desc"] = x.text
				elif x.attrib['name'].upper() == 'DNM':
					comps[name]["dnm"] = True
				elif x.attrib['name'].upper() == 'MPN':
					comps[name]["mpn"] = x.text
				elif p.match(x.attrib['name'].upper()): #MPN[N]
					mpns.append(x.text)


			comps[name]["mpns"] = ",".join(unique(mpns))

			if (comps[name]["mpn"] == None) and (len(mpns) >= 1):
				comps[name]["mpn"] = mpns[0]
				if not mpns[1:]:
					comps[name]["mpns"] = ",".join(mpns[1:])
				else:
					comps[name]["mpns"] = None

	return comps


def group_components_for_bom(components):
	comps = {}
	for key in sorted(components):
		keys_with_same_value = [k for k, v in components.items() if v == components[key]]
		new_key = ",".join(sorted(keys_with_same_value))
		if (new_key not in comps) and (components[key]['dnm'] == False) and (components[key]['mpn'] != None):
			comps[new_key] = components[key]
	return comps


def write_bom(output_file_slug, comps):

	field_names = ['Ref', "Description", 'MPN', 'MPNs', 'Qty']

	with open("{}".format(output_file_slug), 'w') as csvfile:

		bomwriter = csv.DictWriter(
			csvfile, fieldnames=field_names,
			delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		bomwriter.writeheader()

		for k in comps:

			bomwriter.writerow({
				'Ref': k,
				'Description': comps[k]['desc'],
				'MPN': comps[k]['mpn'],
				"MPNs": comps[k]['mpns'],
				'Qty': len(k.split(','))
				})


def parts_with_dnm_attribute(components):
	dnm = []
	for key in components:
		if components[key]["dnm"] == True:
			dnm.append(key)
	return dnm


def parts_with_missing_mpn(components):
	missing_mpn = []
	for key in components:
		if (components[key]["mpn"] is None) and (components[key]["dnm"] is False):
			missing_mpn.append(key)
	return missing_mpn


def quantity_of_parts_with_mpn(components):
	count = 0
	for key in components:
		if components[key]["mpn"] is not None:
			count = count + len(key.split(','))
	return count

def print_list(l):
	l = sorted(l)
	for i, item in enumerate(l):
		print("{:3}: {}".format(i+1, item))


if __name__ == "__main__":

	args = parse_command_line()

	input_file = args.input_file
	output_file = args.output_file

	components = parse_kicad_xml(input_file)
	grouped_components = group_components_for_bom(components)
	write_bom(output_file, grouped_components)

	dnm_parts = parts_with_dnm_attribute(components)
	if len(dnm_parts) > 0:
		print("\n** Info **: skipping {} part(s) with do not mount (DNM) attribute".format(len(dnm_parts)))
		print_list(dnm_parts)

	missing_mpn = parts_with_missing_mpn(components)
	if len(missing_mpn) > 0:
		print("\n** Warning **: there are {} parts without MPNs".format(len(missing_mpn)))
		print_list(missing_mpn)

	print("")
	print("Unique Parts: {}".format(len(grouped_components)))
	print("Parts with MPN: {}".format(quantity_of_parts_with_mpn(grouped_components)))
	print("Parts without MPN: {}".format(len(missing_mpn)))
	print("DNM Parts: {}".format(len(dnm_parts)))
