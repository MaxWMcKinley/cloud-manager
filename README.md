I spent about 10 hours implementing this. I had never used python before this project.  
I used the Click python library to implement my CLI.  
I used code from here for a method to print to stderr: https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python  
I used code from here for a method of checking ip addresses: https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python   


To set up the program:  
1. Clone or unzip the repository
2. Change your directory to the repository root
3. Run: "source env/bin/activate"

Now you can run the program. An example of running one of the commands from the project description:  
"python aggiestack.py config --hardware examples/hdwr-config.txt"

Or if you are running in a bash shell you can change the aggiestack.py file to be executable with:  
"chmod +x aggiestack.py"  
This will allow you to forego the "python" at the beginning of the command:
"./aggiestack.py config --hardware examples/hdwr-config.txt"
