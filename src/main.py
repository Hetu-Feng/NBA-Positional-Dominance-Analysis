import sys
import WebScraping as ws
import DataStoring as ds
import DataModeling as dm

 
def main(argv):
    if len(argv) == 2:
        if argv[1] == '-source=remote':
            print('Gather data from web.')
            records = ws.scrape_all()
            ds.DataStoring(records)
            dm.DataModeling()
        elif argv[1] == '-source=local':
            print('Gather data on disk.')
            dm.DataModeling()
        else: 
            print('Please enter a valid paramater: -source=remote / -source=local.')
    else:
        print('Please enter a valid paramater: -source=remote / -source=local.')

if __name__ == '__main__':
    main(sys.argv)

  
