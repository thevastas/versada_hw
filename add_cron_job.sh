path_to_script=$(find $(pwd) -maxdepth 1 -name "main.py")
crontab -l | grep -v "input.csv" | crontab -
echo "0 17 * * * python $path_to_script -x input.csv" | crontab
