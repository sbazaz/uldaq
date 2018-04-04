# Remove the Python packages
if [ -e "python2_files.txt" ]; then
   echo "Removing Python 2 package"
   cat python2_files.txt | xargs rm -rf
   rm python2_files.txt
fi

echo

if [ -e "python3_files.txt" ]; then
   echo "Removing Python 3 package"
   cat python3_files.txt | xargs rm -rf
   rm python3_files.txt
fi

echo

echo "uldaq Python API uninstall complete."