pip install tmscoring
* have anaconda

pip install numpy
pip install iminuit
pip install Bio
pip install biopython # this might not be needed (should not be needed)
* Change bio folder in Lib to "Bio" instead of "bio" in virtual environment

pip install xlwt

download and install Phenix 

Steps:
  1. python3 -m venv env 
  2. source ./env/bin/activate
  3. For right now manually install requirements above "pip install ..."
  4. Put EMD in input folder. An example has been given of structure.
  5. Ground truth in input folder must be named "native.pdb"
  6. Run
        * python main.py input output -s selections.json -a TMalign 
             -p C:\Users\RyanHarlich\Phenix\phenix-installer-1.16-3549-intel-windows-x86_64\build\bin\phenix.chain_comparison.bat 
        * note: an example selections.json file has been given to show
             how to select starting residue and ending residue
        * note: TMalign make sure to chmod 700
        
Note: 'which python' to make sure using virtual environment

If no selections is given for EMD then all will be selected.

