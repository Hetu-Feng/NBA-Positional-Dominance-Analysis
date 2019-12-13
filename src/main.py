import sys
import WebScraping as ws
import DataStoring as ds
import DataModeling as dm

 
def main(argv):
    if len(argv) == 2:
        if argv[1] == '-source=remote':
            print('Gathering data from web.\n')
            records = ws.scrape_all()
            ds.DataStoring(records)
            dm.DataModeling()
            print('All done! Check the graph in the folder!\n')
            print('Final Conclusion:\n'
                '1. The original assumption is partially confirmed as the result shows that it is the guards that are dominating the league in recent years and centers faded.\n'
                '2. However, since 1998, centers were already not as dominant as guards and forwards, and their dominance was dropping during the year 2000 to 2008 period.\n'
                '3. Centers are making a small comeback after year 2008 and 2009, but they are still down.\n'
                '4. An interesting finding is that forwards were at the level with guards before around year 2008 but started to go down after that time and on the same dominance level as centers till today.\n')


        elif argv[1] == '-source=local':
            print('Gathering data on disk.\n')
            dm.DataModeling()
            print('All done! Check the graph in the folder!\n')
            print('Final Conclusion:\n'
                '1. The original assumption is partially confirmed as the result shows that it is the guards that are dominating the league in recent years and centers faded.\n'
                '2. However, since 1998, centers were already not as dominant as guards and forwards, and their dominance was dropping during the year 2000 to 2008 period.\n'
                '3. Centers are making a small comeback after year 2008 and 2009, but they are still down.\n'
                '4. An interesting finding is that forwards were at the level with guards before around year 2008 but started to go down after that time and on the same dominance level as centers till today.\n')

        else: 
            print('Please enter a valid paramater: -source=remote / -source=local.')
    else:
        print('Please enter a valid paramater: -source=remote / -source=local.')

if __name__ == '__main__':
    main(sys.argv)

  
