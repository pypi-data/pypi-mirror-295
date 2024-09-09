"""
setup.py file for testing birefringence pycbc waveform plugin package
"""

from setuptools import Extension, setup, Command, find_packages

setup (
    packages = find_packages(),
    #py_modules = ['birefringence'],
    #package_dir = {'':'src'},
    #package_dir={'PyTGR': 'src'},
    entry_points = {"pycbc.waveform.fd":["birefringence = tgr.birefringence:gen_waveform",
                                         "massivegraviton = tgr.massivegraviton:gen_waveform",
                                         "fta = tgr.fta:gen_waveform",
                                         "ppe = tgr.ppe:gen_waveform",
                                         "lsa = tgr.lineofsight:gen_waveform"],
                    "pycbc.waveform.length":["birefringence = tgr:length_in_time",
		    			                     "massivegraviton = tgr:length_in_time",
					                         "fta = tgr:length_in_time",
                                             "ppe = tgr:length_in_time",
                                             "lsa = tgr:length_in_time"]}
)
