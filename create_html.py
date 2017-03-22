#!/usr/bin/python
"""
Copyright 2017 University of Cincinnati
All rights reserved. See LICENSE file at:
https://github.com/AS4SR/website
Additional copyright may be held by others, as reflected in the commit history.
"""

import os

gitdir = "/home/spacerobotics/git_pulls/website-master/"
""" for debugging, use this instead (otherwise may overwrite currently-existing files under gitdir of public_html):
html_sitedir = "html_site/"
html_top = html_sitedir + "public_html/"
"""
html_sitedir = "public_html/"
html_top = html_sitedir + "./"

"""
import shutil
# if the directory exists, remove it for new compilation
try:
    treetotest = gitdir + html_sitedir
    os.stat(treetotest)
    shutil.rmtree(treetotest, ignore_errors=True) # removes whole directory tree, ignores read-only files (careful, this is dangerous!!!)
except:
    pass
# thetop fresh directory there 
os.mkdir(html_sitedir)
# Reference: https://docs.python.org/2/library/os.html
"""

# we are going to assume that the directory doesn't exist yet because it's a new wget download-and-unzip
""" as above, already exists...
os.mkdir(gitdir + html_sitedir)
os.mkdir(html_top)
print("initial top-level compilation directory created...")
"""

css_filename = "teststyles3.css"
css_filedir = "test2/"
css_to_use = gitdir + "public_html/" + css_filedir + css_filename

full_templatedir = gitdir + "public_html/" + "_templates/"
html_full_template_pieces = \
['html_full_template.top.0', # then add CSS file name, href="-->THISHERE<--"
 'html_full_template.top.1', # then add body class="-->THISHERE<--"
 'html_full_template.top.2', # then add topofpage stuff (from testtopbar2div.html)
 'html_full_template.top.3', # then add verticalmenubar stuff (from testnavbar2.html)
 'html_full_template.top.4', # then add mainbody stuff (from whatever the latest html file fragment is from the html_create_list)
 'html_full_template.top.5', # then add footer stuff
 'html_full_template.top.6', # then add bottomof page stuff
 'html_full_template.top.7'] # this ends off the html file

"""
html_create_list = \
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
"""

html_create_list = \
[['index','./','index.html','_template_parts/index.part'],
['about','./','about.html','_template_parts/about.part']]

try:
    """ unnecessary, going to copy that over in the largr grab...
    print("copying over CSS file...")
    # copy over the CSS file being used to the html_top directory
    f = open(css_to_use,'r')
    css_filecontents = f.read()
    f.close()
    f = open(html_top + css_filename,'w')
    f.write(css_filecontents)
    f.close()
    print("CSS file copied!")
    """

    print("starting html creation...")
    for i in range(len(html_create_list)):
        print("starting work on " + html_top + html_create_list[i][1] + html_create_list[i][2])
        
        print("creating directory (" + html_top + html_create_list[i][1] + ") that it goes within...")
        # first, try and create the directory the file's gonna reside in, in case it doesn't exist already
        try:
            os.mkdir(html_top + html_create_list[i][1])
        except:
            pass
        print("directory created")
    
        # grab the other file pieces you need on this run:
        print("grabbing pieces...")
        piece = []
        #print(piece)
        # add CSS file name, href="-->THISHERE<--"
        piece.append(css_filedir + css_filename)
        #print(piece)
        # add body class="-->THISHERE<--"
        piece.append(html_create_list[i][0])
        #print(piece)
        # add topofpage stuff (from testtopbar2div.html)
        filename_temp = gitdir + "public_html/" + "_templates/topofpage.part"
        f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
        piece.append(tempholdtext)
        #print(piece)
        # add verticalmenubar stuff (from testnavbar2.html)
        filename_temp = gitdir + "public_html/" + "_templates/verticalmenubar.part"
        f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
        piece.append(tempholdtext)
        #print(piece)
        # add mainbody stuff (from whatever the latest html file fragment is from the html_create_list)
        filename_temp = gitdir + "public_html/" + html_create_list[i][3]
        f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
        piece.append(tempholdtext)
        #print(piece)
        # add footer stuff
        piece.append("testfooter (placeholder text)")
        #print(piece)
        # add bottomofpage stuff
        piece.append("testbottomofpage (placeholder text)")
        #print(piece)
        print("all pieces grabbed!")
        
        # then, stitch the file together:
        print("stitching file together...")
        f = open(full_templatedir + html_full_template_pieces[0],'r');
        filecontents = f.read(); f.close();
        filecontents = filecontents[0:(len(filecontents)-1)]# remove '\n' at end of filecontents fileread
        print("template piece " + str(0) + " stitched...")
        for j in range(len(html_full_template_pieces)-1): # already read 0'th piece of html_full_template_pieces[]
            filecontents += piece[j] # start at 0'th piece
            print("piece " + str(j) + " stitched...")
            f = open(full_templatedir + html_full_template_pieces[j+1],'r');
            filecontents += f.read(); f.close();
            filecontents = filecontents[0:(len(filecontents)-1)]# remove '\n' at end of filecontents fileread
            print("template piece " + str(j+1) + " stitched...")
        print("file stitched!")
    
        # now, write everything to the file
        print("writing "+ html_top + html_create_list[i][1] + html_create_list[i][2] + "...")
        f = open(html_top + html_create_list[i][1] + html_create_list[i][2],'w');
        f.write(filecontents); f.close();
        print(html_top + html_create_list[i][1] + html_create_list[i][2] + " has been written")

    # we're done!
    print("done with html compilation")
    
    print("We're done! Completed writing all files successfully :)")

except:
    print("Error: ran into a problem and crashed!!")

# --EOF--
