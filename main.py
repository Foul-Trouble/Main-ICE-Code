'''Work with your teammate(s) to implement code that solves the following tasks:•.Giventhe following lists of lists [
[1,2,3],[4,5,6],[7,8,9]] do the following:i.Print all the numbers in the list of lists using nested for loops. (
That’s a for loop inside a for loop.)ii.Sum all the numbers in the list of lists and print the sum.iii.Print the
lengthof the list of lists. Notice that the length is not equal to the number of numbersthis time, but instead equal
to the number of lists in the list of lists.iv.Bonus: What if we wanted to find the total number of numbers in the
list of lists, instead of justthe number of lists? Write some code to do this.•We’re going to create a dictionary
that tracks peoples phone numbers. Create a dictionary that has the following pairs:{‘daniel’:’555-5555’,
‘anna’:’555-7777', ‘linus’:’555-6666’}i.Using a for loop, print each of the keys and values for the dictionary (the
names and phone numbers of all the entries), for the entire dictionary.ii.Add a new entry to the dictionary of ‘bob’
with a phone number of ‘555-2222’. iii.Print all the phone numbers in the dictionary, but not the names.iv.Print the
length of the dictionary using the len function.v.Write an if statement that checks to see if ‘daniel’ is in the
dictionary. If it is, print Daniel'sphone number from the dictionary. vi.Print just Linus'sphone numberfrom the
dictionary.vii.Print allthe names (without the phone numbers) in the dictionary.•We’re going to do some graphing
today, and get our feet wet with MatPlotLib. i.The first thing we’ll need to do is install MatPlotLib, to do this,
go to your terminal inpycharm and type:pip install matplotlibii.Once this is done, go into your editor, and import
the matplotlib.pyplot module in particular. A common way of doing this is:import matplotlib.pyplot as pltiii.Now that
we have pyplotimported, we can start plotting data! Let’s give the following a try:1.Plot the sin of all the numbers
from 1 up to 5 against their “x” values.(That is, plot the sin of 1,2,3,4, and 5, against the numbers 1,2,3,
4 and 5.)2.Plot the cos of all numbers from 0up to 30.a.Note: You may wish to use numpy’s built in arange or linspace
for this.3.Plot any quadratic curve. (A simple version would x**2)4.Plot any linear function. (A simple version would
be 2*x + 1)5.Take a list of arbitrary numbers and plot it on a graph vs it’s indexes.3.BONUS:Write some code that
solves the following word problems:•BONUS:Billy Bob is anumbersorting enthusiast;he loves to sort numbers all day
long. We’re going to write a program to help Billy Bob in his sorting endeavors. We want to write a program that
takes in a series of numbers, one after the other, until weinput the number 0. Once we enter the number 0into the
program, the program will stop accepting inputs. At this point, the program should first print all the numbers we
have entered so far in the order that we entered them. It will thentake all the numbers we have entered so far,
and sort them, before printing all the numbers out to the screen in sorted order. This will no doubtsave Billy Bob
many hoursper dayof manuallysorting using pen and paper.•BONUS:Daniel Bob, Billy Bob’s long-lost third cousin (twice
removed), is once again up to no good! The police have contacted you to help track his activities. It turns out
Daniel has been buying cargo vanvehiclesin large quantities andstockpiling them for an unknown nefarious scheme.
Citizens have been reportedly saying, “Dangit! Daniel is back at it again with the white vans!”There is much unrest
in the city due to Daniel’s newest scheme, and you arethe only hope to restore order. The police have given you their
requirements for a program to track all of Daniel’s vans, and it is as follows:You should write a program that takes
in information as inputin a loop until the user indicates they want to stop. The information your program should ask
for is:Thelicenseplateinformation(which isunique for each van),aVIN number (also unique),the company the van was made
by,the model of van being used, and the cargo capacity by volume in cubic centimeters.After this input is collected,
the user should be asked if they want to stop collecting input, or if they want to continuewith theloop.Once the user
indicates they wantto stop entering information about vans, the nested dictionary should be printed to the
screen.•BONUS:The police are really satisfied with your work, they havebeen able to itemize the vans much more
quickly thanks to your quick thinkingand programming prowess. The police have noticed, though, that some of Daniel’s
vans were already indexed by an olddatabase, and they want your help converting them to the new dictionary format,
since it’s easier for their systems to work with. There is a problem though, there are some mistakes in the old data.
For all of thevans made by“ford”, the cargo capacityis off by a factor of two, and for all the “chevy”vans,
it’s off by exactly 16 cm squared in each case. The police have the old data in a file called “old_data.dat”in the
following format:licence_plate;vin_number;company_name;model_name;volumeYourjob is to parse the data out of this
fileinto a nested dictionary structure as before. Then, you should correct any mistakes in the data (so if the model
name if ford, multiply the volume by 2and store it back in the dictionary, if the model is chevy, add 16 to the
volume and store it back in the dictionary). After this is done, print the nested dictionary to the screen as
beforeso that the police can work with it. The police will want to use this program to process many files,
but examplecontent for aold_data.dat file is provided in the paragraph
belowABC123;48123658485411439;ford;transit;5150834ABC213;48123656789411439;ford;transit;5150834ABC321
;48123658480812539;ford;transit;4991995ACB123;48123658485555539;ford;transit;4991995ACB213;23423659999922539;chevy
;express;10230017ACB321;23423659999922539;chevy;express;10229999CAB321;9998888777774471;nissan;nv;9335559CAB312
;9998888776665582;nissan;nv;11567589 '''