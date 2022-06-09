#Assumptions for COMP1531 Flockr Assignment

Our database will consist three variables; two integers (num_users, num_channels) and 
and a data dictionary that is split into two main keys (users and channels).

We assume that first and last name does not need to be stored, only the handle that is made from both.

Token is not stored in the data structure for iteration 1. Instead, it is made from the u_id by adding the letter 'f'.

User and channel ID's start at 0 and are incremented by one when create / register functions are called. 

We assume that only the exceptions listed in the specification of the project are needed to be implemented  

When a channel is created, the token that is passed into the function
channels_create(), causes the corresponding user to automatically join and 
become the original owner of the channel.

If a channel exists with zero members, it will remain active in the database as the owner
of flockr has the ability to remedy the situation with global permissions.




