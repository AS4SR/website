#!/usr/bin/python

import os
os.mkdir(html_site_dir)
os.mkdir(html_site_dir)

gitdir = "/home/spacerobotics/git_pulls/website-master/"
html_sitedir = "html_site/"
html_top = html_sitedir + "public_html/"

/*
import shutil
# if the directory exists, remove it for new compilation
try:
    os.stat(html_site_dir)
    shutil.rmtree(html_site_dir, ignore_errors=True) # removes whole directory tree, ignores read-only files (careful, this is dangerous!!!)
except:
    pass
# thetop fresh directory there 
os.mkdir(html_site_dir)
# Reference: https://docs.python.org/2/library/os.html
*/

# we are going to assume that the directory doesn't exist yet because it's a new wget download-and-unzip
os.mkdir(html_site_dir)
os.mkdir(html_top)

css_filename = "teststyles3.css"
css_filedir = "test2/"
css_to_use = gitdir + "public_html/" + css_filedir + css_filename

full_templatedir = gitdir + "_templates/"
html_full_template_pieces = \
['html_full_template.top.0', # then add CSS file name, href="-->THISHERE<--"
 'html_full_template.top.1', # then add body class="-->THISHERE<--"
 'html_full_template.top.2', # then add topofpage stuff (from testtopbar2div.html)
 'html_full_template.top.3', # then add verticalmenubar stuff (from testnavbar2.html)
 'html_full_template.top.4', # then add mainbody stuff (from whatever the latest html file fragment is from the html_create_list)
 'html_full_template.top.5', # then add footer stuff
 'html_full_template.top.6', # then add bottomof page stuff
 'html_full_template.top.7'] # this ends off the html file

/*html_create_list = \
[['index','./','index.html','_template_parts/index.part'],
['about','./','about.html','_template_parts/about.part'],
['resources','./','resources.html','_template_parts/resources.part'],
['robots','./','robots.html','_template_parts/robots.part'],
['archived_robots','archived/','robots.html','_template_parts/archived_robots.part'],
['archived','./','archived.html','_template_parts/archived.part'],
['testcssdiv','test2/','testcssdiv.html','_template_parts/testcssdiv.part'],
[testcssdiv_clone','test2/','testcssdiv_clone.html','_template_parts/testcssdiv_clone.part'],
['testnavbar2','test2/','testnavbar2.html','_template_parts/testnavbar2.part'],
['testtopbar2div','test2/','testtopbar2div.html','_template_parts/testtopbar2div.part']]*/

html_create_list = \
[['index','./','index.html','_template_parts/index.part'],
['about','./','about.html','_template_parts/about.part']]

try:
    # copy over the CSS file being used to the html_top directory
    f = open(css_to_use,'r')
    css_filecontents = f.read()
    f.close()
    f = open(html_top + css_filename,'w')
    f.write(css_filecontents)
    f.close()

    for i in range(len(html_create_list)):
        # first, try and create the directory the file's gonna reside in, in case it doesn't exist already
        try:
            os.mkdir(html_site_dir+html_create_list[1])
        except:
            pass
    
        # grab the other file pieces you need on this run:
        piece = []
        # add CSS file name, href="-->THISHERE<--"
        piece[0] = css_filedir + css_filename
        # add body class="-->THISHERE<--"
        piece[1] = html_create_list[i][0]
        # add topofpage stuff (from testtopbar2div.html)
        filename_temp = gitdir + "public_html/" + "_templates/topofpage.part"
        f = open(filename_temp,'r');
        piece[2] = f.read(); f.close();
        # add verticalmenubar stuff (from testnavbar2.html)
        filename_temp = gitdir + "public_html/" + "_templates/verticalmenubar.part"
        f = open(filename_temp,'r');
        piece[3] = f.read(); f.close();
        # add mainbody stuff (from whatever the latest html file fragment is from the html_create_list)
        filename_temp = gitdir + "public_html/" + html_create_list[i][3]
        f = open(filename_temp,'r');
        piece[4] = f.read(); f.close();
        # add footer stuff
        piece[5] = "testfooter"
        # add bottomofpage stuff
        piece[6] = "testbottomofpage"
   
        # then, stitch the file together:
        f = open(full_templatedir + html_full_template_pieces[0],'r');
        filecontents = f.read(); f.close();
        for j in range(len(html_full_template_pieces)-1): # already read 0'th piece of html_full_template_pieces[]
            filecontents += piece[j] # start at 0'th piece
            f = open(full_templatedir + html_full_template_pieces[j+1],'r');
            filecontents += f.read(); f.close();
        f = open(full_templatedir + html_full_template_pieces[len(html_full_template_pieces)-1],'r');
        filecontents += f.read(); f.close();
    
        # now, write everything to the file
        f = open(html_top + html_create_list[i][1] + html_create_list[i][2],'w');
        f.write(filecontents); f.close();

    # we're done!
    print("We're done! Completed writing all files successfully :)")

except:
    print("Error: ran into a problem and crashed!!")

# --EOF--
