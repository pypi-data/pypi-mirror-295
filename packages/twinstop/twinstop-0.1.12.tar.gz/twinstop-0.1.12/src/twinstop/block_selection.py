# -*- coding: utf-8 -*-

import os
import numpy as np
from Bio.Align import substitution_matrices

twinstop_libpath = os.path.dirname(os.path.realpath(__file__)) + "/data_files/"


def block_dict(query_seq, subj_seq, dictionary):
    """
    Takes two protein sequences (one from the query and the other from the subject),
    divides them into blocks according to the stops '*' present in both and then
    saves in a list of dictionaries the start, end and score (matrix Blosum62)
    of each block. Afterward, the block with better score is selected and the
    data of the score, start, end and sequence from both query and subject is
    updated in the general dataframe.

    Parameters
    ----------
    query_seq : String
        Aligned protein sequence of the query
    subj_seq : String
        Aligned protein sequence of the subject
    dictionary : Dictionary of tuples
        Matrix Blosum62 values

    Returns
    -------
    best_block[0] : Dictionary with the 'Start', 'End' and 'Score' values of the
    best scored fragment of each alignment.
    """

    list_stops = list()  # create a list to save stops index

    for index, x in enumerate(query_seq):
        # we count the start and the end of the sequence always as stops
        if index == 0 or index == len(query_seq) - 1:
            # if x != '*' and subj_seq[index] != '*':
            list_stops.append(index)
            continue
        # save all the indexes of stops
        if x == "*" or subj_seq[index] == "*":
            list_stops.append(index)

    block_dict_list = list()  # creates a list
    for idx, x in enumerate(list_stops):
        if x == list_stops[-1]:
            break  # necessary to skip an error
        block_dict = dict()  # creates a dictionary
        # we skip the 1st and last index of the fragments (stops)
        ######################################
        #### MM: never scoring the first and last position --> fix it
        block_dict["Align_Start"] = x + 1
        block_dict["Align_End"] = list_stops[idx + 1]
        block_dict["Score"] = score(
            query_seq[x : list_stops[idx + 1]],
            subj_seq[x : list_stops[idx + 1]],
            dictionary,
        )
        block_dict_list.append(block_dict)  # create a list of dictionaries
    # dictionaries of each alignment are sorted by 'Score'
    # reverse=True to have the best scored one at the beginning
    # lambda input: output
    best_block = sorted(block_dict_list, key=lambda x: x["Score"], reverse=True)

    return best_block[0]  # return the dictionary with the values of the best fragment


def score(query_frag, subj_frag, dictionary):
    """
    Calculates the score using matrix Blosum62

    Parameters
    ----------
    query_frag : String
        Protein sequence from the query
    subj_frag : String
        Protein sequence from the subject
    dictionary : Dictionary
        Matrix Blosum Values

    Returns
    -------
    Score : Int
        Value according to matrix Blosum62
    """

    score = 0
    for index, x in enumerate(query_frag):
        if x == "-" or subj_frag[index] == "-":
            continue
        score += dictionary[(x, subj_frag[index])]

    return score


def dictionary_seleno(biopython_format=False):
    """
    Creates a dictionary of tuples with the values of the BLOSUM62 Matrix.

    Parameters
    ----------
    biopython_format : bool, default False
        returns a Bio.Align.substitution_matrices.Array instead of default

    Returns
    -------
    dictionary_sel : <dict>
        Dictionary of tuples with the values of the BLOSUM62 Matrix.
    """

    dictionary_sel = dict()

    with open(twinstop_libpath + "Matrix_BLOSUM62sel.txt", "r") as fr:
        for index, row in enumerate(fr):
            # creates a list, using ' ' as sep.
            spt = row.split(" ")
            # deletes blank spaces.
            spt = list(filter(None, spt))
            if index == 0:
                # delete empty spaces.
                header = [x.strip() for x in spt]
                continue
            # deletes '\n' characters.
            spt = [x.strip() for x in spt]
            # converts the values (<str>) into <int>.
            ints = [int(x) for x in spt[1:]]
            keys = [(spt[0], aa) for aa in header]
            # creation of the dictionary:
            for ik, k in enumerate(keys):
                dictionary_sel[k] = ints[ik]
    if biopython_format:
        blosum = substitution_matrices.load("BLOSUM62")
        alphabet = blosum.alphabet + 'U'
        mdata = [  [float(dictionary_sel[(a1, a2)])   for a2 in alphabet] for a1 in alphabet]
        return substitution_matrices.Array( alphabet=alphabet, data=np.array(mdata) )

    return dictionary_sel
