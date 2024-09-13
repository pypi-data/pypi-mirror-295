# twinstop
Twinstop identifies selenoproteins in close related transcriptomes

# Installation
In a new conda environment, run::

   conda install -c conda-forge -c bioconda -c mmariotti    twinstop

## Installation troubleshooting
If solving takes forever, we recommend switching to mamba instead.
That is, uninstall conda; install mamba; create a new environment; then run the command::

   mamba install -c conda-forge -c bioconda -c mmariotti    twinstop


As of this writing, the command above correctly installs twinstop in a linux64 system.
In case it fails of any unresolved conflicts, try to download the file requirements.txt,
and run this to create a copy of a verified conda environment::

  conda create --name twinstop --file requirements.txt

Then activate the new env twinstop, then run the install command above.

# Usage
To see usage, run::

  twinstop -h


# Authors
Sergio Sanchez Moragues and Marco Mariotti
