TripGenie

Objective and Current MVP

	The objective of this project is to build a route planner for a trip. When the destination, starting point, and car information is inputted, it will provide a detailed route with the cheapest gas stations and any possible preferred stops along the way. The MVP will be able to provide a working google maps route link, with gas stations added with accurate prices. Additionally other functions could include possible tourist attractions based on interests, along with hotels and restaurants based on the users interest.

Progress and Technical Approach

	Currently, we have built a basic trip planner that is able to provide a working google maps route based on the starting point, destination, along with basic car information such as the year, model, and brand. The route comes preinstalled with gas station stops, and will also recommend other gas stations on the chance that you prefer a particular brand. The interface is simple but is able to have the route embedded into it. 
	We did this by creating two different datasets, one with the fuel economy of different cars from a variety of brands, and then one of gas station locations and their prices. Our program pulls from these datasets whenever you input your information into it in order to create your route. Codex is used to help revise and create the script as needed in order to make it more efficient and user friendly.
	A lot of progress has been made in the last few weeks. Initially a few APIs were used rather than datasets in order to pull the information on the route and gas stations, such as their location and prices. Unfortunately, the program struggled to use these APIs and further investigation showed that a few of them were not able to provide specific data, only general averages. An example of this could be when the program was only able to pull the average of gas stations nationwide, which caused it to create imperfect routes or give errors when recommending gas stations. Due to this a large dataset of gas stations was created, and while this doesn’t provide accurate live data, it does fulfill the role of what will later be an API once we find one that can provide our needed information accurately. Along with this, at the beginning we had no good interface for our program, but over time have been able to create an interface that is capable of having google maps embedded in it.
  
Current Limitations and Open Risks

	There are a few limitations in our program, mainly with the datasets we use. Because we use a hand written dataset for the gas stations, the prices aren’t accurate, along with opening and closing times. For the vehicles, we are constrained to the vehicles in the database, if the user inputted a car that wasn’t in there then the program wouldn’t be able to help them. Overall, these two problems are the biggest limitations in our project and the current obstacle preventing our program from being truly accurate and able to provide fully live data.
  
Plan for Phase 3

This leads us to our next steps and phase 3. We plan to fully integrate APIs for gas station, car information, along with various route information that can better help our program provide recommendations for the user. Several APIs for the fuel economy information of cars can be found on government websites and are free. Google also has APIs to better help our program locate and sift through gas stations and their prices. Furthermore the interface will be refined and made more user friendly so they are less constrained to text boxes.

Additional Notes

	README.md file contains all the instructions on how to run the MVP for phase 2 of the project. 
  MVP phase 2 code is "TripGenie_Phase_2.zip"
  Google doc link to view Evidence of Progress: https://docs.google.com/document/d/1IOJPG903AtgxQ7L8L6Oa2WjAECzXVeQKQSUeMZJlce8/edit?tab=t.0

Group Members
Jonathon Jones - jmjone97@asu.edu 
Daniel Romero - dromer39@asu.edu 
Ethan Lim - ethanlim@asu.edu 
Clint Allen - ccalle15@asu.edu 
