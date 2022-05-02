import subprocess


process = subprocess.run(['python3', '../Pricing/plotting.py', 'C', 'range', '30D', 'delta' ,'450'])
process.stdout