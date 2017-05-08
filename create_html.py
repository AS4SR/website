#!/usr/bin/python
"""
Copyright 2017 University of Cincinnati
All rights reserved. See LICENSE file at:
https://github.com/AS4SR/website
Additional copyright may be held by others, as reflected in the commit history.
"""

import os
import sys

#local_compile_check = "no" # for live website, use this
local_compile_check = "yes" # for local directory checks of website, not-live, use this -- note that body images &etc. will not work

website_top="http://www.ase.uc.edu/~spacerobotics/"

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

#css_filename = "teststyles3.css"
#css_filedir = "test2/"
#css_to_use = gitdir + "public_html/" + css_filedir + css_filename
css_filename = "styles.css"
#css_filedir = "./"
css_filedir = ""
css_to_use = gitdir + "public_html/" + css_filedir + css_filename

full_templatedir = gitdir + "_templates/"
html_full_template_pieces = \
['html_full_template.top.0a',
# then add title of webpage, <title>--THISHERE--</title>
 'html_full_template.top.0b',
# then add CSS file name, href="-->THISHERE<--"
 'html_full_template.top.1',
# then add body class="-->THISHERE<--"
 'html_full_template.top.2',
# then add topofpage stuff (from testtopbar2div.html)
 'html_full_template.top.3',
# then add verticalmenubar stuff (from testnavbar2.html)
 'html_full_template.top.4',
# then add mainbody stuff (from whatever the latest html file fragment is from the html_create_list)
 'html_full_template.top.5',
# then add footer stuff
 'html_full_template.top.6',
# then add bottomof page stuff
 'html_full_template.top.7'] # this ends off the html file

# [ul_class_level_in_menubar, name_in_css_file , outfile_location_rel_to_public_html , outfilename , .part_filename_plus_location , name_in_vertical_menubar_and_htmlpage_title]
html_create_list = \
[['','','./','custom404.html','_template_parts/custom404.part','404 Error'], # note that this isn't added to the CSS or menubar list
 ['level1','index','','index.html','_template_parts/index.part','Home'],
 ['level1','about','','about.html','_template_parts/about.part','About'],
 ['level1','resources','','resources.html','_template_parts/coming_soon.part','Resources'],
 ['level2','robots','','robots.html','_template_parts/coming_soon.part','Robots'],
 ['level2','archived_robots','archived/','robots.html','_template_parts/coming_soon.part','Archived Robots'],
 ['level1','archived','','archived.html','_template_parts/coming_soon.part','Archived Projects'],
 ['level2','later','archived_projects/','later.html','_template_parts/coming_soon.part','...']]
titlerider = " - AS4SR Lab, University of Cincinnati"

#
# create "verticalmenubar.part" as verticalmenubar_str for use!!
#

verticalmenubar_part_1 = """<!-- modified heavily from: http://stackoverflow.com/questions/7055024/how-to-store-nav-bar-in-one-file -->
  <!-- <div id="menu"> -->"""
verticalmenubar_part_2 = """    </ul>
  <!-- </div> -->
"""
verticalmenubar_part = []
verticalmenubar_part.append(verticalmenubar_part_1)
N = len(html_create_list)
i = 0
tabs = 0 # 4 spaces per level
level = 0
while (i < N):
    if (html_create_list[i][0] == ''):
        i += 1 # then ignore that part / don't add it to the menubar
        continue
    elif (html_create_list[i][0] == 'level1'):
        tabs = 1
        prevlevel = level
        level = 1
    elif (html_create_list[i][0] == 'level2'):
        tabs = 2
        prevlevel = level
        level = 2

    if (level > prevlevel): # assumes only 2 levels
        verticalmenubar_part.append("\n" + " "*(tabs*4) + """<ul class="%s">\n""" % html_create_list[i][0])
    elif (level < prevlevel): # assumes only 2 levels
        verticalmenubar_part.append("""</li>\n""" + " "*((tabs+1)*4) + """</ul>\n""" + " "*(tabs*4+2) + """</li>\n""")
    else: #elif (level == prevlevel):
        verticalmenubar_part.append("""</li>\n""")
    verticalmenubar_part.append(" "*(tabs*4+2) + \
        """<li class="%s"><a href='%s%s%s'>%s</a>""" % (html_create_list[i][1],website_top,html_create_list[i][2],html_create_list[i][3],html_create_list[i][5]))
    i += 1
# need to close out blocks at the end
if (html_create_list[i-1][0] == 'level2'):
    verticalmenubar_part.append("""</li>\n""" + " "*(tabs*4) + """</ul>\n""" + " "*(tabs*4-2) + """</li>\n""")
    tabs = 1
    prevlevel = level
    level = 1
if (html_create_list[i-1][0] == 'level1'):
    verticalmenubar_part.append("""</li>\n""" + " "*(tabs*4) + """</ul>\n""" + " "*(tabs*4-2) + """</li>\n""")
    tabs = 0
    prevlevel = level
    level = 0
verticalmenubar_part.append(verticalmenubar_part_2)
# then print verticalmenubar_part to file named "vertical_menubar.part"? or just concatenate all strings?
verticalmenubar_part_str = ""
for i in range(len(verticalmenubar_part)):
	verticalmenubar_part_str += verticalmenubar_part[i]
#print(verticalmenubar_part_str)

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
    
    #
    # create styles.css file
    #
    print("starting CSS file creation...")
    
    print("creating directory (" + html_top + html_sitedir + ") that it goes within...")
    # first, try and create the directory the file's gonna reside in, in case it doesn't exist already
    try:
        os.mkdir(html_top + html_sitedir)
    except:
        pass
    print("directory created")
    
    # grab the other file pieces you need on this run:
    print("grabbing pieces...")
    piece = []
    # add beginning of CSS file stuff
    filename_temp = gitdir + "_templates/styles.css.part.1"
    f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
    piece.append(tempholdtext)
    #print(piece)
    # add mainbody stuff (from whatever the latest html file fragment is from the html_create_list)
    holdstr = "" # don't put this in unless it's not the first one
    for i in range(len(html_create_list)):
        if (len(html_create_list[i][1]) > 0): # skip if doesn't have a name_in_css_file (string is != "")
            piece.append(holdstr + "body.%s li.%s a" % (html_create_list[i][1],html_create_list[i][1]))
            holdstr = ",\n"
            #print(piece)
    # add end of CSS file stuff
    filename_temp = gitdir + "_templates/styles.css.part.2"
    f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
    piece.append(tempholdtext)
    #print(piece)
    print("all pieces grabbed!")
    
    # then, stitch the file together:
    print("stitching file together...")
    filecontents = ""
    for j in range(len(piece)):
        filecontents += piece[j]
        print("piece " + str(j) + " stitched...")
    print("file stitched!")
    
    # update location on links for things if testing locally-only, not compiling for live-website
    if (local_compile_check == "no"): # for live website, use this
        pass # is already set up for this
    else: #if (local_compile_check == "yes"): # for local directory checks of website, not-live, use this -- note that body images &etc. will not work
        replace_website_top_with_this = "file://" + gitdir + "public_html/"
        filecontents = filecontents.replace(website_top,replace_website_top_with_this)

    # now, write everything to the file
    filelocation_str = css_to_use
    print("writing "+ filelocation_str + "...")
    f = open(filelocation_str,'w');
    f.write(filecontents); f.close();
    print(filelocation_str + " has been written")

    # we're done!
    print("done with CSS file compilation")

    #
    # now, get the majority of html files stitched together
    #

    print("starting html creation...")
    for i in range(len(html_create_list)):
        print("starting work on " + html_top + html_create_list[i][2] + html_create_list[i][3])
        
        print("creating directory (" + html_top + html_create_list[i][2] + ") that it goes within...")
        # first, try and create the directory the file's gonna reside in, in case it doesn't exist already
        try:
            os.mkdir(html_top + html_create_list[i][2])
        except:
            pass
        print("directory created")
    
        # grab the other file pieces you need on this run:
        print("grabbing pieces...")
        piece = []
        #print(piece)
        # then add title of webpage, <title>--THISHERE--</title>
        piece.append(html_create_list[i][5] + titlerider)
        #print(piece)
        # add CSS file name, href="-->THISHERE<--"
        piece.append(website_top + css_filedir + css_filename) # for live website, use this
        #print(piece)
        # add body class="-->THISHERE<--"
        piece.append(html_create_list[i][1])
        #print(piece)
        # add topofpage stuff (from testtopbar2div.html)
        filename_temp = gitdir + "_templates/topofpage.part"
        f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
        piece.append(tempholdtext)
        #print(piece)
        # add verticalmenubar stuff (from testnavbar2.html)
        #filename_temp = gitdir + "_templates/verticalmenubar.part"
        #f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
        #piece.append(tempholdtext)
        piece.append(verticalmenubar_part_str) # now creating this inside the file!
        #print(piece)
        # add mainbody stuff (from whatever the latest html file fragment is from the html_create_list)
        filename_temp = gitdir + html_create_list[i][4]
        print("filenametemp = " + filename_temp)
        f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
        piece.append(tempholdtext)
        #print(piece)
        # add footer stuff
        filename_temp = gitdir + "_templates/footer.part"
        f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
        piece.append(tempholdtext)
        #print(piece)
        # add bottomofpage stuff
        piece.append("") #("testbottomofpage (placeholder text)")
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
        
        # update location on links for things if testing locally-only, not compiling for live-website
        if (local_compile_check == "no"): # for live website, use this
            pass # is already set up for this
        else: #if (local_compile_check == "yes"): # for local directory checks of website, not-live, use this -- note that body images &etc. will not work
            replace_website_top_with_this = "file://" + gitdir + "public_html/"
            filecontents = filecontents.replace(website_top,replace_website_top_with_this)
    
        # now, write everything to the file
        filelocation_str = html_top + html_create_list[i][2] + html_create_list[i][3]
        print("writing "+ filelocation_str + "...")
        f = open(filelocation_str,'w');
        f.write(filecontents); f.close();
        print(filelocation_str + " has been written")

    # we're done!
    print("done with html compilation")
    
    print("We're done! Completed writing all files successfully :)")

except:
    print("Error: ran into a problem and crashed!!")

# --EOF--
