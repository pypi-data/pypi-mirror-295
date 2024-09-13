#!/usr/bin/env -u python -S
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 12:18:00 2022

@author: Toño
"""

from easyterm import command_line_options, write

# from Bio import pairwise2
import pandas as pd, subprocess, shlex, multiprocess as mp, numpy as np, os

# from Bio.SubsMat import MatrixInfo as matlist
# from denovo_selenoproteins import dictionary_seleno


def mafft(joined_df):
    # out_mafft = '/users-d2/EGB4-guest/seleno_prediction/outputs/out_mafft'
    # mafft alignment
    assert len(joined_df) == 1
    i = joined_df.index[0]
    out_temp = "fasta_mafft_" + str(i)
    # for i in joined_df.index:
    # to run mafft we need a fasta file with the subject and query
    # protein sequences.
    with open(out_temp, "w") as fw:
        fw.write(f">Subject\n")
        fw.write(f"{joined_df.at[i, 'Subj_align_prot_seq']}\n")
        fw.write(f">Query\n")
        fw.write(f"{joined_df.at[i, 'Q_align_prot_seq']}\n")
    # --anysymbol is used to recognize 'U'
    # ???
    # print(joined_df.loc[i, 'Subj_align_prot_seq'])
    # print(joined_df.loc[i, 'Q_align_prot_seq'])
    # print(f'Out temp = {out_temp}')
    mafft_subj = "mafft --auto --anysymbol " + out_temp
    subj_mafft_list = shlex.split(mafft_subj)
    y = subprocess.run(subj_mafft_list, capture_output=True)
    if y.returncode != 0:
        print(y.stderr, y.stdout)
        raise Exception()
    os.remove(out_temp)
    # we need to decode() the standard output to get the results.
    outfile = y.stdout.decode().split("\n")
    # print(outfile)
    temp_mafft = ""
    for x in outfile:
        if x == ">Subject" or x == "":
            continue
        elif x == ">Query":
            temp_mafft += f"\n"
        else:
            temp_mafft += f"{x}"
    # print(f'Temp mafft = {temp_mafft}')
    list_mafft = temp_mafft.split("\n")
    # print(f'List mafft = {list_mafft}')
    # substitute the sequences without gaps for the new one with gaps.
    try:
        joined_df.at[i, "Subj_align_prot_seq"] = list_mafft[0]
        joined_df.at[i, "Q_align_prot_seq"] = list_mafft[1]
    except:
        print(f"Joined_df = {joined_df}")
        raise SystemExit

    return joined_df


# def pairwise_alignment(extended_hits_df, matrix):
#     '''
#     This function runs Pairwise global alignment tool to insert gaps in the aligned
#     protein sequences.
#
#     Parameters
#     ----------
#     extended_hits_df : <pd.DataFrame>
#         Dataframe with the extended hits.
#     matrix : <dict>
#         Dictionary with the BLOSUM62 matrix values.
#
#     Returns
#     -------
#     joined_df : <pd.DataFrame>
#         Dataframe with gaps in the protein sequences (if alignment is improved).
#     '''
#
#     # write(f'Pairwise alignment')
#     for i in extended_hits_df.index:
#         # -7 is the cost to open a gap, -1 is the cost to extend it.
#         # pairwise2.align.global parameters:
#         # d     A dictionary returns the score of any pair of characters.
#         # s     Same open and extend gap penalties for both sequences.
#         alignment = pairwise2.align.globalds(extended_hits_df.at[i, 'Q_align_prot_seq'],
#                                              extended_hits_df.at[i, 'Subj_align_prot_seq'],
#                                              matrix, -7, -1, one_alignment_only=True)
#         # only the best scored alignment is selected.
#         extended_hits_df.at[i, 'Q_align_prot_seq'] = alignment[0][0]
#         extended_hits_df.at[i, 'Subj_align_prot_seq'] = alignment[0][1]
#
#     return extended_hits_df

# matrix = dictionary_seleno()

# def mp_pairwise_alignment(x):
#     return pairwise_alignment(x, matrix)

# def missing_alignments(pre_df, post_df, timeout, n_cpu):
#     # time_1 = time.time()
#     mis_align = pre_df[~pre_df['ID'].isin(post_df['ID'])]
#     # print(f'Mis_align: {mis_align}')
#     # print(f'Mis_align: {mis_align.shape[0]}\n')
#     # print(f'Time used: {time.time() - time_1}')
#     # sys.exit(1)
#     results = multiprocessing(mis_align, mafft, n_cpu, timeout)
#     # if mis_align.shape[0] != results.shape[0]:
#     #     # print(f'Mis_align: {mis_align.shape[0]}\n')
#     #     # print(f'Results: {results.shape[0]}')
#     #     mis_align_2 = mis_align[~mis_align['ID'].isin(results['ID'])]
#     #     # time_1 = time.time()
#     #     results_2 = multiprocessing(mis_align_2, mafft, n_cpu, timeout)
#     #     # print(f'Mafft time for {len(mis_align_2)} alignments: {time.time() - time_1}')
#     #     if mis_align_2.shape[0] != results_2.shape[0]:
#     #         # print(f'Mis_align_2: {mis_align_2.shape[0]}\n')
#     #         # print(f'Results_2: {results_2.shape[0]}')
#     #         mis_align_3 = mis_align_2[~mis_align_2['ID'].isin(results_2['ID'])]
#     #         # print(f'Mis_align_3: {mis_align_3.shape[0]}\n')
#     #         print(f'Mafft did not finished on time,\nProblematic lines:\n{mis_align_3}')
#     #     else:
#     #         post_df = pd.concat(results_2, axis=0, ignore_index=True)
#     #         print(f'Second pairwise worked with timeout {timeout}')
#     # else:
#     #     post_df = pd.concat(results, axis=0, ignore_index=True)
#     #     print(f'Second pairwise worked with timeout {timeout}')
#
#     return results

def chunkify(df, n):
    """Split DataFrame into n chunks."""
    k, m = divmod(len(df), n)
    return (df.iloc[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))

def multiprocessing(chunkdf, func, n_cpu, timeout):
    with mp.Pool(processes=n_cpu) as pool:
        # lock = mp.Manager().Lock()
        # shared_list = manager.list()
        results = []
        completed_results = []
        for row in chunkify(chunkdf, len(chunkdf)):
            result = pool.apply_async(func, args=(row,))
            results.append(result)
        for result in results:
            try:
                completed_results.append(result.get(timeout=timeout))
            except mp.context.TimeoutError:
                print(f"A result took too long")
                pass

        df_chunk = pd.concat(completed_results, axis=0, ignore_index=True)
    return df_chunk


# def main():
#     help_msg = """ This program allows us to test which alignment
#     method is faster.
#
#     ### Input/Output:
#     -df : dataframe with the sequences to align
#
#     ### Options:
#     -print_opt: print currently active options
#     -h | --help: print this help and exit"""
#
#     def_opt = {'pre_df': '/home/ssanchez/seleno_prediction/outputs/Mus_musculus_vs_Homo_sapiens/ext_orfs.tsv',
#                'post_df': '/home/ssanchez/seleno_prediction/outputs/Mus_musculus_vs_Homo_sapiens/aln_orfs.tsv'}

# opt = command_line_options(def_opt, help_msg)

# pre_df = pd.read_csv(opt['pre_df'],
#                      sep='\t', header=0, index_col=False)
# post_df = pd.read_csv(opt['post_df'],
#                       sep='\t', header=0, index_col=False)
#
# output = missing_alignments(pre_df, post_df, 2.5)
# output.to_csv('/home/ssanchez/seleno_prediction/outputs/recovered_align.tsv',
#               sep='\t', header=0, index=False)

# if __name__ == '__main__':
#     main()
