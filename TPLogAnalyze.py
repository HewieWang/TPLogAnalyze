import requests,os,json
from datetime import datetime,timedelta
from urllib.parse import urlparse,unquote
from multiprocessing.pool import ThreadPool
from moz_sql_parser import parse

print('********************************')
print('*                              *')
print('*    ThinkPHP3.2 LogAnalyze    *')
print('*                              *')
print('********************************')

def Detect(LogFile):
	if not LogFile.endswith('.log'):
		print("Url Must End with .log")
		return False
		pass
	pass

def gen_dates(b_date, days):
    day = timedelta(days=1)
    for i in range(days):
        yield b_date + day*i

def get_date_list(start=None, end=None):
    if start is None:
        start = datetime.strptime("2020-09-26", "%Y-%m-%d")
    if end is None:
        end = datetime.now()
    data = []
    for d in gen_dates(start, (end-start).days):
        data.append(d)
    return data

def GetFileList(path,hostname):
	print('Start...')
	files= os.listdir(path)
	for file in files:
		LogAnalyze(hostname+'/Logfile/'+file,hostname)
		pass
	print('Mission Completed!')
	pass

def download(file_name,hostname,url,LogDictory='Logfile'):
    try:
    	if not os.path.exists(hostname+'/'+LogDictory+''):
    		os.makedirs(hostname+'/'+LogDictory+'')
    	if not os.path.isfile(hostname+'/'+LogDictory+'/'+file_name):
    		r = requests.get(url, stream=True)
	    	with open(hostname+'/'+LogDictory+'/'+file_name, 'wb') as f:
	            for chunk in r.iter_content(chunk_size=1024 * 1024):
	                if chunk:
	                    f.write(chunk)
	    	pass
    except Exception as e:
    	raise e

def WriteIn(strs,path):
	if not strs in open(path,encoding='UTF-8',errors='ignore'):
		f=open(path,'a',errors='ignore')
		f.write(strs+'\n')
		f.close()
		pass
	pass

def GetRoute(strs,hostname,routes='Routes.txt'):
	if not os.path.exists(hostname+'/'+routes):
		f=open(hostname+'/'+routes,'w')
		f.close()
		pass
	if '[ 20' in strs:
		if '/' in strs:
			WriteIn(strs[strs.index('/'):],hostname+'/'+routes)
			pass
		pass
	pass

def SqlCollect(strs,hostname,routes='Sqls.txt'):
	if not os.path.exists(hostname+'/'+routes):
		f=open(hostname+'/'+routes,'w')
		f.close()
		pass
	if 'SQL:' in strs:
		sql=strs[:strs.index('[')][strs.index(':'):].strip(':')
		res=parse(sql)
		WriteIn(res['from'],hostname+'/Tables.txt')
		WriteIn(sql,hostname+'/'+routes)
		pass

def AnalyzeSql(sql):
	tables = ', '.join(extract_tables(sql))
	print('Tables: {}'.format(tables))
	pass

def LogAnalyze(filepath,hostname):
	for line in open(filepath,encoding='UTF-8'):
		GetRoute(line,hostname)
		SqlCollect(line,hostname)
		AnalyzeSql(sql)
		pass
	pass

def generate_log_url(LogFile,During):
	hostname=urlparse(LogFile).netloc
	print("Domain: "+hostname)
	if not os.path.exists(hostname):
		os.makedirs(hostname)
	#urls=[]
	print("Download Start...")
	for x in get_date_list():
		f=str(x.year)+'_'+str(x.month).zfill(2)+'_'+str(x.day).zfill(2)+'.log'
		filename=f[2:]
		print(LogFile[:-12]+filename)
		download(filename,hostname,LogFile[:-12]+filename)
		pass
	print('Download End')
	GetFileList(hostname+'/Logfile',hostname)
	pass


if __name__ == "__main__":
	LogFile=input("LogFileUrl:")
	Detect(LogFile)
	generate_log_url(LogFile,1)
