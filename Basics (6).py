#!/usr/bin/env python
# coding: utf-8

# # Explorting and Analyzing Data in SQL
# 
# For this project, I will practice exploring and analyzing data in SQL. I will be working with data from the [CIA World Factbook](https://www.cia.gov/library/publications/the-world-factbook/). 

# In[1]:


get_ipython().run_cell_magic('capture', '', '%load_ext sql\n%sql sqlite:///factbook.db')


# In[8]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\n    FROM facts\n    lIMIT 5')


# I will now calculate some summary statistics and look for any outlier countries

# In[9]:


get_ipython().run_cell_magic('sql', '', '\nSELECT MIN(population), MAX(population),\n    MIN(population_growth), MAX(population_growth)\n    FROM facts')


# This seems odd. Both of the minimum and maximum populations are off. I will use subqueries to zoom in on just these countries without using the specific values. 

# In[10]:


get_ipython().run_cell_magic('sql', '', 'SELECT name, MIN(population)\n    FROM facts\n    WHERE POPULATION == (SELECT MIN(population)\n                        FROM facts\n                        );')


# Antarctica is not a country. This explains the population of 0. 

# In[11]:


get_ipython().run_cell_magic('sql', '', 'SELECT name, MAX(population)\n    FROM facts\n    WHERE POPULATION == (SELECT MAX(population)\n                        FROM facts\n                        );')


# And the large value comes from the world population. I will recalculate the summary statistics from before but exclude the row for the world. 

# In[18]:


get_ipython().run_cell_magic('sql', '', "\nSELECT MIN(population), MAX(population),\n    MIN(population_growth), MAX(population_growth)\n    FROM facts\n    WHERE name <> 'World';")


# I will now look at the population and area columns. I want to find countried that are densely populated. First, I will look at averages.

# In[20]:


get_ipython().run_cell_magic('sql', '', '\nSELECT ROUND(AVG(population), 2), ROUND(AVG(area),2)\n    FROM facts;')


# I will now look for countried that have a higher than average population and and lower than average area. 

# In[21]:


get_ipython().run_cell_magic('sql', '', 'SELECT name, population, area\n    FROM facts\n    WHERE population > (SELECT AVG(population)\n                       FROM facts)\n    AND area < (SELECT AVG(area)\n               FROM facts);')


# These results make sense. 

# In[ ]:




