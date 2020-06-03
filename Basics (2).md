
# Explorting and Analyzing Data in SQL

For this project, I will practice exploring and analyzing data in SQL. I will be working with data from the [CIA World Factbook](https://www.cia.gov/library/publications/the-world-factbook/). 


```python
%%capture
%load_ext sql
%sql sqlite:///factbook.db
```




    'Connected: None@factbook.db'




```python
%%sql
SELECT *
    FROM facts
    lIMIT 5
```

    Done.





<table>
    <tr>
        <th>id</th>
        <th>code</th>
        <th>name</th>
        <th>area</th>
        <th>area_land</th>
        <th>area_water</th>
        <th>population</th>
        <th>population_growth</th>
        <th>birth_rate</th>
        <th>death_rate</th>
        <th>migration_rate</th>
    </tr>
    <tr>
        <td>1</td>
        <td>af</td>
        <td>Afghanistan</td>
        <td>652230</td>
        <td>652230</td>
        <td>0</td>
        <td>32564342</td>
        <td>2.32</td>
        <td>38.57</td>
        <td>13.89</td>
        <td>1.51</td>
    </tr>
    <tr>
        <td>2</td>
        <td>al</td>
        <td>Albania</td>
        <td>28748</td>
        <td>27398</td>
        <td>1350</td>
        <td>3029278</td>
        <td>0.3</td>
        <td>12.92</td>
        <td>6.58</td>
        <td>3.3</td>
    </tr>
    <tr>
        <td>3</td>
        <td>ag</td>
        <td>Algeria</td>
        <td>2381741</td>
        <td>2381741</td>
        <td>0</td>
        <td>39542166</td>
        <td>1.84</td>
        <td>23.67</td>
        <td>4.31</td>
        <td>0.92</td>
    </tr>
    <tr>
        <td>4</td>
        <td>an</td>
        <td>Andorra</td>
        <td>468</td>
        <td>468</td>
        <td>0</td>
        <td>85580</td>
        <td>0.12</td>
        <td>8.13</td>
        <td>6.96</td>
        <td>0.0</td>
    </tr>
    <tr>
        <td>5</td>
        <td>ao</td>
        <td>Angola</td>
        <td>1246700</td>
        <td>1246700</td>
        <td>0</td>
        <td>19625353</td>
        <td>2.78</td>
        <td>38.78</td>
        <td>11.49</td>
        <td>0.46</td>
    </tr>
</table>



I will now calculate some summary statistics and look for any outlier countries


```python
%%sql

SELECT MIN(population), MAX(population),
    MIN(population_growth), MAX(population_growth)
    FROM facts
```

    Done.





<table>
    <tr>
        <th>MIN(population)</th>
        <th>MAX(population)</th>
        <th>MIN(population_growth)</th>
        <th>MAX(population_growth)</th>
    </tr>
    <tr>
        <td>0</td>
        <td>7256490011</td>
        <td>0.0</td>
        <td>4.02</td>
    </tr>
</table>



This seems odd. Both of the minimum and maximum populations are off. I will use subqueries to zoom in on just these countries without using the specific values. 


```python
%%sql
SELECT name, MIN(population)
    FROM facts
    WHERE POPULATION == (SELECT MIN(population)
                        FROM facts
                        );
```

    Done.





<table>
    <tr>
        <th>name</th>
        <th>MIN(population)</th>
    </tr>
    <tr>
        <td>Antarctica</td>
        <td>0</td>
    </tr>
</table>



Antarctica is not a country. This explains the population of 0. 


```python
%%sql
SELECT name, MAX(population)
    FROM facts
    WHERE POPULATION == (SELECT MAX(population)
                        FROM facts
                        );
```

    Done.





<table>
    <tr>
        <th>name</th>
        <th>MAX(population)</th>
    </tr>
    <tr>
        <td>World</td>
        <td>7256490011</td>
    </tr>
</table>



And the large value comes from the world population. I will recalculate the summary statistics from before but exclude the row for the world. 


```python
%%sql

SELECT MIN(population), MAX(population),
    MIN(population_growth), MAX(population_growth)
    FROM facts
    WHERE name <> 'World';
```

    Done.





<table>
    <tr>
        <th>MIN(population)</th>
        <th>MAX(population)</th>
        <th>MIN(population_growth)</th>
        <th>MAX(population_growth)</th>
    </tr>
    <tr>
        <td>0</td>
        <td>1367485388</td>
        <td>0.0</td>
        <td>4.02</td>
    </tr>
</table>



I will now look at the population and area columns. I want to find countried that are densely populated. First, I will look at averages.


```python
%%sql

SELECT ROUND(AVG(population), 2), ROUND(AVG(area),2)
    FROM facts;
```

    Done.





<table>
    <tr>
        <th>ROUND(AVG(population), 2)</th>
        <th>ROUND(AVG(area),2)</th>
    </tr>
    <tr>
        <td>62094928.32</td>
        <td>555093.55</td>
    </tr>
</table>



I will now look for countried that have a higher than average population and and lower than average area. 


```python
%%sql
SELECT name, population, area
    FROM facts
    WHERE population > (SELECT AVG(population)
                       FROM facts)
    AND area < (SELECT AVG(area)
               FROM facts);
```

    Done.





<table>
    <tr>
        <th>name</th>
        <th>population</th>
        <th>area</th>
    </tr>
    <tr>
        <td>Bangladesh</td>
        <td>168957745</td>
        <td>148460</td>
    </tr>
    <tr>
        <td>Germany</td>
        <td>80854408</td>
        <td>357022</td>
    </tr>
    <tr>
        <td>Japan</td>
        <td>126919659</td>
        <td>377915</td>
    </tr>
    <tr>
        <td>Philippines</td>
        <td>100998376</td>
        <td>300000</td>
    </tr>
    <tr>
        <td>Thailand</td>
        <td>67976405</td>
        <td>513120</td>
    </tr>
    <tr>
        <td>United Kingdom</td>
        <td>64088222</td>
        <td>243610</td>
    </tr>
    <tr>
        <td>Vietnam</td>
        <td>94348835</td>
        <td>331210</td>
    </tr>
</table>



These results make sense. 


```python

```
