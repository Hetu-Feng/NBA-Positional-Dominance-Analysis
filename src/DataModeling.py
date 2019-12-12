import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def DataModeling():

	## Model Data
	## Convert stored data into DataFrames
	ori_position_1_df = pd.read_csv('ori_position_1.csv')
	ori_position_2_df = pd.read_csv('ori_position_2.csv')
	ori_FGA_df = pd.read_csv('ori_FGA.csv')
	ori_USG_df = pd.read_csv('ori_USG.csv')
	ori_salary_df = pd.read_csv('ori_salary.csv')
	ori_draft_df = pd.read_csv('ori_draft.csv')
	ori_EV_df = pd.read_csv('ori_EV.csv')


	## Make a copy of the original data frame
	position_1_df = ori_position_1_df.copy()
	FGA_df = ori_FGA_df.copy()
	USG_df = ori_USG_df.copy()
	salary_df = ori_salary_df.copy()
	draft_df = ori_draft_df.copy()
	EV_df = ori_EV_df.copy()


	## Data Cleaning
	## combine SF and PF as F (forwards), SG and PG as G (guards)
	position_1_df = position_1_df.replace(['SF', 'PF'], 'F')
	position_1_df = position_1_df.replace(['SG', 'PG'], 'G')

	## Clean alternative position csv
	position_2_df = ori_position_2_df.copy()
	position_2_df = position_2_df[['player_name', 'position']]
	position_2_df['player_name'] = position_2_df['player_name'].apply(lambda x: x.split('\\')[0])
	position_2_df['player_name'] = position_2_df['player_name'].apply(lambda x: x.strip('*'))
	position_2_df = position_2_df.drop_duplicates(subset = 'player_name', keep='first')
	position_2_df['position'] = position_2_df['position'].apply(lambda x: x.split('-')[0])
	position_2_df = position_2_df.replace(['SF', 'PF'], 'F')
	position_2_df = position_2_df.replace(['SG', 'PG'], 'G')

	## delete players that have games played less than 30 and minutes played per game less than 15 minutes
	FGA_df.games_played = FGA_df.games_played.astype(int)
	FGA_df = FGA_df[FGA_df.games_played >= 30]
	FGA_df.minutes_played_per_game = FGA_df.minutes_played_per_game.astype(float)
	FGA_df = FGA_df[FGA_df.minutes_played_per_game >= 15.0]
	#FGA_df.info()
	FGA_df = FGA_df.drop('games_played', axis = 1)
	FGA_df = FGA_df.drop('minutes_played_per_game', axis = 1)

	## delete players that have games played less than 30 and total minutes played less than 15 minutes
	USG_df.games_played = USG_df.games_played.astype(int)
	USG_df = USG_df[USG_df.games_played >= 30]
	USG_df.total_minutes_played = USG_df.total_minutes_played.astype(float)
	USG_df = USG_df[USG_df.total_minutes_played >= 450.0]
	#USG_df.info()
	USG_df = USG_df.drop('games_played', axis = 1)
	USG_df = USG_df.drop('total_minutes_played', axis = 1)

	## Sort FGA DataFrame according to its values group by years
	FGA_df.field_goal_attempt = FGA_df.field_goal_attempt.astype(float)
	FGA_df = FGA_df.groupby(['year']).apply(lambda x: x.sort_values(["field_goal_attempt"], ascending = False)).reset_index(drop=True)

	## Sort USG DataFrame according to its values group by years 
	USG_df.usage_percentage = USG_df.usage_percentage.astype(float)
	USG_df = USG_df.groupby(['year']).apply(lambda x: x.sort_values(["usage_percentage"], ascending = False)).reset_index(drop=True)

	## Sort salary DataFrame according to its top 80 values group by years
	salary_df.salary = salary_df.salary.astype(int)
	salary_df = salary_df.groupby(['year']).apply(lambda x: x.sort_values(["salary"], ascending = False)).reset_index(drop=True)
	salary_df = salary_df.groupby(['year']).head(80)

	## Integrate draft DataFrame and EV DataFrame and sort the new DataFrame according to its values group by year
	new_draft_df = pd.merge(draft_df, EV_df, on = 'pick_rank')
	new_draft_df = new_draft_df.drop(['pick_rank'], axis = 1)
	new_draft_df = new_draft_df[['player_name', 'expected_value', 'year']]
	new_draft_df.expected_value = new_draft_df.expected_value.astype(float)
	new_draft_df = new_draft_df.groupby(['year']).apply(lambda x: x.sort_values(["expected_value"], ascending = False)).reset_index(drop=True)


	## Integrate all data into four data frames: position vs FGA, position vs USG, position vs salary, position vs draft
	## Integrate position_1_df and position_2_df into position_df
	position_df = position_1_df.append(position_2_df)


	## position vs FGA
	position_FGA_df = pd.merge(position_df, FGA_df, on = 'player_name')
	position_FGA_df = position_FGA_df.drop('player_name', axis = 1)
	position_FGA_df = position_FGA_df[['position', 'field_goal_attempt', 'year']]
	position_FGA_df = position_FGA_df.groupby(['year']).apply(lambda x: x.sort_values(["field_goal_attempt"], ascending = False)).reset_index(drop=True)

	## position vs USG
	position_USG_df = pd.merge(position_df, USG_df, on = 'player_name')
	position_USG_df = position_USG_df.drop('player_name', axis = 1)
	position_USG_df = position_USG_df[['position', 'usage_percentage', 'year']]
	position_USG_df = position_USG_df.groupby(['year']).apply(lambda x: x.sort_values(["usage_percentage"], ascending = False)).reset_index(drop=True)

	## position vs salary
	position_salary_df = pd.merge(position_df, salary_df, on = 'player_name')
	position_salary_df = position_salary_df.drop('player_name', axis = 1)
	position_salary_df = position_salary_df[['position', 'salary', 'year']]
	position_salary_df = position_salary_df.groupby(['year']).apply(lambda x: x.sort_values(["salary"], ascending = False)).reset_index(drop=True)

	## position vs draft
	position_draft_df = pd.merge(position_df, new_draft_df, on = 'player_name')
	position_draft_df = position_draft_df.drop(['player_name'], axis = 1)
	position_draft_df = position_draft_df[['position', 'expected_value', 'year']]
	position_draft_df = position_draft_df.groupby(['year']).apply(lambda x: x.sort_values(["expected_value"], ascending = False)).reset_index(drop=True)


	## Keep grouping data frames, make relationships between position vs average FGA, average USG, average salary, and sum of expected value from draft
	## position vs average FGA
	position_avgFGA_df = position_FGA_df.groupby(['year', 'position'], as_index = False).mean()
	position_avgFGA_df = position_avgFGA_df.pivot(index = 'year', columns = 'position', values = 'field_goal_attempt')
	## position vs average USG
	position_avgUSG_df = position_USG_df.groupby(['year', 'position'], as_index = False).mean()
	position_avgUSG_df = position_avgUSG_df.pivot(index = 'year', columns = 'position', values = 'usage_percentage')
	## position vs average salary
	position_avgsalary_df = position_salary_df.groupby(['year', 'position'], as_index = False).mean()
	position_avgsalary_df = position_avgsalary_df.pivot(index = 'year', columns = 'position', values = 'salary')
	## position vs average expected value from draft
	position_sumdraft_df = position_draft_df.groupby(['year', 'position'], as_index = False).sum()
	position_sumdraft_df = position_sumdraft_df.pivot(index = 'year', columns = 'position', values = 'expected_value')


	## Export DataFrame to csv files
	## First update after data cleaning 
	# position_1_df.to_csv('position_1.csv')
	# position_2_df.to_csv('position_2.csv')
	# FGA_df.to_csv('FGA.csv')
	# USG_df.to_csv('USG.csv')
	# salary_df.to_csv('salary.csv')
	# draft_df.to_csv('draft.csv')
	# EV_df.to_csv('EV.csv')
	# new_draft_df.to_csv('new_draft.csv')

	# Second update after combining tabels 
	# position_df.to_csv('position.csv')
	# position_FGA_df.to_csv('position_FGA.csv')
	# position_USG_df.to_csv('position_USG.csv')
	# position_salary_df.to_csv('position_salary.csv')
	# position_draft_df.to_csv('position_draft.csv')

	## Thrid update after reshaping tables
	position_avgFGA_df.to_csv('position_avgFGA.csv')
	position_avgUSG_df.to_csv('position_avgUSG.csv')
	position_avgsalary_df.to_csv('position_avgsalary.csv')
	position_sumdraft_df.to_csv('position_sumdraft.csv')


	## Data Visualization
	fig, axes = plt.subplots(2, 2, figsize = (25, 10))
	fig.subplots_adjust(wspace = 0.2, hspace = 0.5)

	## Set up legend
	positions = ['C', 'F', 'G']

	for i in range(3):
	    axes[0, 0].plot(position_avgFGA_df.iloc[:,i], label=positions[i])
	    axes[0, 1].plot(position_avgUSG_df.iloc[:,i], label=positions[i])
	    axes[1, 0].plot(position_avgsalary_df.iloc[:,i], label=positions[i])
	    axes[1, 1].plot(position_sumdraft_df.iloc[:,i], label=positions[i])

	## Upper left, visualize players' average field goal attempts vs position over year
	axes[0, 0].legend()
	axes[0, 0].set_title('Average Field Goal Attempt vs Position over year')
	axes[0, 0].set_xlabel('year')
	axes[0, 0].set_ylabel('average FGA')
	x_ticks_1 = np.arange(1998, 2019, 1)
	y_ticks_1 = np.arange(6, 11, 0.5)
	axes[0, 0].set_xticks(x_ticks_1)
	axes[0, 0].set_yticks(y_ticks_1)

	## Upper right, visualize players' average usage percentange vs position over year 
	axes[0, 1].legend()
	axes[0, 1].set_title('Average Usage Percentange vs Position over year')
	axes[0, 1].set_xlabel('year')
	axes[0, 1].set_ylabel('average USG%')
	x_ticks_2 = np.arange(1998, 2019, 1)
	y_ticks_2 = np.arange(15, 22, 1)
	axes[0, 1].set_xticks(x_ticks_2)
	axes[0, 1].set_yticks(y_ticks_2)

	## Bottom left, visualize players' average salaries vs position over year 
	axes[1, 0].legend()
	axes[1, 0].set_title('Average Salary vs Position over year')
	axes[1, 0].set_xlabel('year')
	axes[1, 0].set_ylabel('average salary (ten million)')
	x_ticks_3 = np.arange(1998, 2019, 1)
	y_ticks_3 = np.arange(5000000, 25000000, 1000000)
	axes[1, 0].set_xticks(x_ticks_3)
	axes[1, 0].set_yticks(y_ticks_3)

	## Bottom right, visualize sum of players' expected values in draft vs position over year 
	axes[1, 1].legend()
	axes[1, 1].set_title("Sum of Draft Expected Value vs Position over year")
	axes[1, 1].set_xlabel('year')
	axes[1, 1].set_ylabel('sum of EV')
	x_ticks_4 = np.arange(1998, 2019, 1)
	y_ticks_4 = np.arange(100, 1000, 100)
	axes[1, 1].set_xticks(x_ticks_4)
	axes[1, 1].set_yticks(y_ticks_4)

	## Export figure 
	#fig.show()
	fig.savefig('Visualization')

