**Tournament**
* 3/24/2016 - Initial creation.

Richard E. Moore - [nano.moore@gmail.com](mailto:nano.moore@gmail.com)

For Udacity's *Full Stack Web Developer Nanodegree* second project, Tournament Results

**NOTE**: Target environment is Python 2.7.1

**TO RUN:**
1. Configure the Vagrant VM per the project guideline: https://classroom.udacity.com/nanodegrees/nd004/parts/0041345404/modules/353202897075461/lessons/3521918727/concepts/35196892840923
2. Unpack all files into the tournament subdirectory of the vagrant folder. Files are:
tournament.py
tournament.sql
tournament_test.py
2. From the Vagrant VM, navigate to the vagrant/tournament directory with command: cd /vagrant/tournament
3. To initialize the database:
   a. Enter command: psql 
   b. Enter command: \i tournament.sql
   c: Exit psql with command: \q
4. To run the test, use command: tournament_test.py
