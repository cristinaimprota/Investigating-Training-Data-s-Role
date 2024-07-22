import sys
import os
import numpy as np
from crystal_bleu import *


def calc_EM(hyps, refs):
	scores = []
	for hyp, ref in zip(hyps, refs):
		hyp_tokens = hyp.split()
		ref_tokens = ref.split()
		if hyp_tokens == ref_tokens:
			scores.append(1)
		else:
			scores.append(0)
	mean_em = np.mean(scores)
	formatted_score='EM:{0:.2f}%'.format(mean_em * 100)
	print(formatted_score)
	return formatted_score

def calc_crystalBLEU(hyps, refs, re_compute_ngrams: bool):
	cache_folder = "crystal_cache"
	if re_compute_ngrams:
		if not os.listdir(cache_folder):
			print("No files to delete. Will compute trivially shared ngrams")
		else:
			print("ngrams files deleted. Will compute trivially shared ngrams")
			files = os.listdir(cache_folder)
			for file in files:
				file_name = os.path.join(cache_folder, file)
				os.remove(file_name)
	else:
		print("Loading trivially shared ngrams")

	trivial_ngrams = compute_trivially_shared_ngrams(hyps, "python", cache_folder)
	scores = compute_crystal_bleu(refs, hyps, trivial_ngrams, "python")
	mean_crystal = np.mean(scores)
	min_crystal = np.min(scores)
	max_crystal = np.max(scores)
	median_crystal = np.median(scores)
	q1_crystal = np.percentile(scores, 25)
	q3_crystal = np.percentile(scores, 75)
	formatted_score = (f'\nCrystalBLEU: {mean_crystal * 100:.2f}% (min: {min_crystal:.3f}, max: {max_crystal:.3f}, median: {median_crystal:.3f}, Q1: {q1_crystal:.3f}, Q3: {q3_crystal:.3f})')
	print(formatted_score)
	return formatted_score


def read_json_singlefile(filename):
	hyps = []
	refs = []

	with open(filename, 'r') as hyps_f:
		data = json.load(hyps_f)
		hyps = [pred['prediction'] for pred in data]
	with open(filename, 'r') as refs_f:
		data = json.load(refs_f) 
		refs = [ref['reference'] for ref in data]
	return hyps, refs
		

if __name__ == '__main__':
	"""
		Read with the correct function to parse input file
	"""

	total_hyps = []
	total_refs = []
	
	total_hyps, total_refs = read_json_singlefile('')	# Filename containing both predictions and references

	print(f"Number of predictions: {len(total_hyps)}")
	print(f"Number of references: {len(total_refs)}")


	for i in range(0, 10):
		print(f"Prediction: {total_hyps[i]}\n")
		print(f"Reference: {total_refs[i]}\n")
	
	calc_crystalBLEU(total_hyps, total_refs, True)		
	calc_EM(total_hyps, total_refs)
