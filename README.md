# JobberFiller
Proof-Of-Concept script to fill Jobber entries using Selenium

# Important Note
This script is *NOT MEANT* for you to cheat on your company's hours. 

The generate_entry and get_deviated_time functions are there only to reduce the time spent on filling the majority of work days where you work the normal hours, and to not make it always follow the same pattern (i.e., by deviating the minutes a little).

If you use this to pretend that you worked more than you did, I *trully* hope you get fired.

The sole purpose of this program is to aid in the slow, time consuming task of filling Jobber, specially if, like me, you always forgot to fill it on a daily basis and have to do all at once at the end of the month.

# Usage

## Dependencies

workalendar: https://pypi.python.org/pypi/workalendar/0.1

selenium: https://pypi.python.org/pypi/selenium


## Variables

Fill the variables with the correct values.


### email
Holds your email address, used to login to Jobber.

### password
Holds your jobber password, in base64. To generate one, simply execute 'echo YOUR_PASSWORD | base64' and paste the result in this variable.

### first_date and last_date
The date were it will start and stop filling things up. I recommend doing it from the start of the month to the end, and not going through months.

### daily_deviation
A tuple containing the minium and maximum minute range for deviation.

### use_custom_default
Normally, if the script were to generate entries, it would go with 'General' for category and a single dot ('.') for text. This overrides that.

### custom_default_category
The first distinguishable part of the custom category.

### custom_default_text
The custom default text.

### cal
This variable holds the "workalendar" object with the holidays of your location. Check https://pypi.python.org/pypi/workalendar/0.1 for possible values and remember to import it.

### vacancy
A list, containing the dates were you were on vacancy, if any.

### fill_weekends
A boolean specifying if the script should feel weekends normally. Note that days on exceptional_dates will *ALWAYS* be filled.

### fill_holidays
A boolean specifying if the script should feel holidays normally. Note that days on exceptional_dates will *ALWAYS* be filled.

### exceptional_only
If the script should *NOT* generate any default entries and just fill the dates specified on *exceptional_dates*.

### exceptional_dates
Add exceptional dates (e.g. dates where you trully want to specify the times) in the following format:
'YYYY/mm/dd': [('CATEGORY', 'NOTES', 'START_TIME', 'END_TIME')]

On CATEGORY, you just need to specify the first distinguishable part of the string, as in '#9 -', or 'General'
Hours need to follow the format HH.MM, as in 9.00, or HH only.

If you add an hour without minutes (e.g. 9), get_deviated_time will be called, using daily_deviation to randomly choose a minute.

'2015/07/31': [('#80 -', 'Did something', '6.00', '9.00'), ('#9 -', 'Did something else', '10.00', '13.00')]

Just add one per line and you should be ok, you can add more than one entry per day as normal, just dont expect me to check if you are overlapping things.

### engine
The engine/driver that Selenium should use. I recommend either 'chrome' of 'phantomjs'. 'firefox' is REALLY, *REALLY* slow.

For Chrome, note that besides Chrome itself you also need chromedriver: https://code.google.com/p/selenium/wiki/ChromeDriver

For PhantomJS, check http://phantomjs.org/

## Running

To run the program, simply call python jobber_filler.py, after filling up all the variables.








