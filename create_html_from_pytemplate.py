#!/usr/bin/python
"""
Copyright 2017 University of Cincinnati
All rights reserved. See LICENSE file at:
https://github.com/AS4SR/website
Additional copyright may be held by others, as reflected in the commit history.
"""

import os
import sys
from string import Template
# see the tutorial for examples of using templating:
# -- https://wiki.python.org/moin/Templating

#
# create "verticalmenubar.part" as verticalmenubar_str for use!!
#
def create_and_return_verticalmenubar(html_create_list,website_top):
    extra = " "*8 # set to "" for effectively level-start count from left side of html file
    verticalmenubar_part_1 = """<!-- modified heavily from: http://stackoverflow.com/questions/7055024/how-to-store-nav-bar-in-one-file -->\n""" + extra + " "*4 + """<!-- <div id="menu"> -->"""
    verticalmenubar_part_2 = extra + " "*4 + """</ul>\n""" + extra + " "*4 + """<!-- </div> -->
    """
    verticalmenubar_part = []
    verticalmenubar_part.append(verticalmenubar_part_1)
    N = len(html_create_list)
    i = 0
    tabs = 0 # 4 spaces per level
    level = 0
    while (i < N):
        [ul_class_level_in_menubar, name_in_css_file , outfile_location_rel_to_public_html , outfilename , \
            part_filename_plus_location , name_in_vertical_menubar_and_htmlpage_title] = html_create_list[i]
        
        if (ul_class_level_in_menubar == ''):
            i += 1 # then ignore that part / don't add it to the menubar
            continue
        elif (ul_class_level_in_menubar == 'level1'):
            tabs = 1
            prevlevel = level
            level = 1
        elif (ul_class_level_in_menubar == 'level2'):
            tabs = 2
            prevlevel = level
            level = 2

        if (level > prevlevel): # assumes only 2 levels
            verticalmenubar_part.append("\n" + extra + " "*(tabs*4) + """<ul class="%s">\n""" % ul_class_level_in_menubar)
        elif (level < prevlevel): # assumes only 2 levels
            verticalmenubar_part.append("""</li>\n""" + extra + " "*((tabs+1)*4) + """</ul>\n""" + extra + " "*(tabs*4+2) + """</li>\n""")
        else: #elif (level == prevlevel):
            verticalmenubar_part.append("""</li>\n""")
        verticalmenubar_part.append(extra + " "*(tabs*4+2) + \
            """<li class="%s"><a href='%s%s%s'>%s</a>""" % (name_in_css_file,website_top,outfile_location_rel_to_public_html,outfilename,name_in_vertical_menubar_and_htmlpage_title))
# if want to include _target="???" ("_blank","_top",etc.), then define variable 'thetarget' and:
#        verticalmenubar_part.append(extra + " "*(tabs*4+2) + \
#            """<li class="%s"><a href='%s%s%s' _target="%s">%s</a>""" % #(name_in_css_file,website_top,outfile_location_rel_to_public_html,outfilename,***THE_TARGET***,name_in_vertical_menubar_and_htmlpage_title))
        i += 1
    # need to close out blocks at the end
    ul_class_level_in_menubar_LAST = html_create_list[i-1][0]
    if (ul_class_level_in_menubar_LAST == 'level2'):
        verticalmenubar_part.append("""</li>\n""" + extra + " "*(tabs*4) + """</ul>\n""" + extra + " "*(tabs*4-2) + """</li>\n""")
        tabs = 1
        prevlevel = level
        level = 1
    if (ul_class_level_in_menubar_LAST == 'level1'):
        verticalmenubar_part.append("""</li>\n""" + extra + " "*(tabs*4) + """</ul>\n""" + extra + " "*(tabs*4-2) + """</li>\n""")
        tabs = 0
        prevlevel = level
        level = 0
    verticalmenubar_part.append(verticalmenubar_part_2)
    # then print verticalmenubar_part to file named "vertical_menubar.part"? or just concatenate all strings?
    verticalmenubar_part_str = "".join(verticalmenubar_part)
    #print(verticalmenubar_part_str)
    return verticalmenubar_part_str

def create_css_file_and_write_to_disk(html_top,html_sitedir,gitdir,html_create_list,local_compile_check,website_top,css_to_use):
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
    
    # read in CSS file template for fill-in
    filename_temp = gitdir + "_templates/styles.css.template"
    f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
    csstemplate = Template(tempholdtext)
    
    # prepare mainbody stuff (from whatever the latest html file fragment is from the html_create_list)
    holdstr = "" # don't put this in unless it's not the first one
    for i in range(len(html_create_list)):
        name_in_css_file = html_create_list[i][1]
        if (len(name_in_css_file) > 0): # skip if doesn't have a name_in_css_file (string is != "")
            piece.append(holdstr + "body.%s li.%s a" % (name_in_css_file,name_in_css_file))
            holdstr = ",\n"
            #print(piece)
    
    print("all pieces grabbed!")
    
    # then, stitch the file together:
    print("stitching file together...")
    # do string substitution:
    filecontents = csstemplate.safe_substitute({"CSSLICLASSTAGS": "".join(piece)})
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

def create_html_file_and_write_to_disk(html_top,html_create_list_piece,full_templatedir,html_full_template,titlerider,website_top,css_filedir,css_filename,gitdir,local_compile_check):

    [ul_class_level_in_menubar, name_in_css_file , outfile_location_rel_to_public_html , outfilename , \
        part_filename_plus_location , name_in_vertical_menubar_and_htmlpage_title] = html_create_list_piece

    print("starting work on " + html_top + outfile_location_rel_to_public_html + outfilename)

    print("creating directory (" + html_top + outfile_location_rel_to_public_html + ") that it goes within...")
    # first, try and create the directory the file's gonna reside in, in case it doesn't exist already
    try:
        os.mkdir(html_top + outfile_location_rel_to_public_html)
    except:
        pass
    print("directory created")

    # read in html file template for fill-in
    #filename_temp = gitdir + "_templates/html_full.template"
    filename_temp = full_templatedir + html_full_template
    f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
    htmltemplate = Template(tempholdtext)
    
    # grab the other file pieces you need on this run:
    print("grabbing pieces...")
    html_replace_dict = dict()
    # $PAGETITLE = title of webpage, <title>--THISHERE--</title>
    html_replace_dict.update( {"PAGETITLE": name_in_vertical_menubar_and_htmlpage_title + titlerider} )
    # $CSSFILE = CSS file name, href="-->THISHERE<--"
    html_replace_dict.update( {"CSSFILE": website_top + css_filedir + css_filename} ) # for live website, use this
    # $BODYCLASS =  body class="-->THISHERE<--"
    html_replace_dict.update( {"BODYCLASS": name_in_css_file} )
    # $TOPOFPAGE = topofpage stuff (from testtopbar2div.html)
    filename_temp = gitdir + "_templates/topofpage.part"
    f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
    tempholdtext = tempholdtext.replace("\n","\n"+" "*4) # offset each line by 4 spaces from left side of html file
    html_replace_dict.update( {"TOPOFPAGE": tempholdtext} )
    # $VERTICALMENUBAR = verticalmenubar stuff (from testnavbar2.html)
    #filename_temp = gitdir + "_templates/verticalmenubar.part"
    #f = open(filename_temp,'r'); verticalmenubar_part_str = f.read(); f.close();
    verticalmenubar_part_str = create_and_return_verticalmenubar(html_create_list,website_top)
    html_replace_dict.update( {"VERTICALMENUBAR": verticalmenubar_part_str} )
    # $MAINBODY = mainbody stuff (from whatever the latest html file fragment is from the html_create_list)
    filename_temp = gitdir + part_filename_plus_location
    print("filenametemp = " + filename_temp)
    f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
    tempholdtext = tempholdtext.replace("\n","\n"+" "*4) # offset each line by 4 spaces from left side of html file
    html_replace_dict.update( {"MAINBODY": tempholdtext} )
    # $FOOTER = footer stuff
    filename_temp = gitdir + "_templates/footer.part"
    f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
    tempholdtext = tempholdtext.replace("\n","\n"+" "*8) # offset each line by 8 spaces from left side of html file
    html_replace_dict.update( {"FOOTER": tempholdtext} )
    # $BOTTOMOFPAGE = bottomof page stuff
    html_replace_dict.update( {"BOTTOMOFPAGE": ""} ) #("testbottomofpage (placeholder text)")
    # this ends off the html file
    print("all pieces grabbed!")
    
    # then, stitch the file together:
    print("stitching file together...")
    # do string substitution:
    filecontents = htmltemplate.safe_substitute(html_replace_dict)
    print("file stitched!")
    
    # update location on links for things if testing locally-only, not compiling for live-website
    if (local_compile_check == "no"): # for live website, use this
        pass # is already set up for this
    else: #if (local_compile_check == "yes"): # for local directory checks of website, not-live, use this -- note that body images &etc. will not work
        replace_website_top_with_this = "file://" + gitdir + "public_html/"
        filecontents = filecontents.replace(website_top,replace_website_top_with_this)

    # now, write everything to the file
    filelocation_str = html_top + outfile_location_rel_to_public_html + outfilename
    print("writing "+ filelocation_str + "...")
    f = open(filelocation_str,'w');
    f.write(filecontents); f.close();
    print(filelocation_str + " has been written")

if __name__ == '__main__':
    local_compile_check = "no" # for live website, use this
    #local_compile_check = "yes" # for local directory checks of website, not-live, use this -- note that body images &etc. will not work

    website_top="http://www.ase.uc.edu/~spacerobotics/"

    gitdir = "/home/spacerobotics/git_pulls/website-master/"
    """ for debugging, use this instead (otherwise may overwrite currently-existing files under gitdir of public_html):
    html_sitedir = "html_site/"
    html_top = html_sitedir + "public_html/"
    """
    html_sitedir = "public_html/"
    html_top = html_sitedir + "./"

    # we are going to assume that the directory doesn't exist yet because it's a new wget download-and-unzip

    css_filename = "styles.css"
    #css_filedir = "./"
    css_filedir = ""
    css_to_use = gitdir + "public_html/" + css_filedir + css_filename

    full_templatedir = gitdir + "_templates/"
    html_full_template = 'html_full.template'
    # will require the following:
    # $PAGETITLE = title of webpage, <title>--THISHERE--</title>
    # $CSSFILE = CSS file name, href="-->THISHERE<--"
    # $BODYCLASS =  body class="-->THISHERE<--"
    # $TOPOFPAGE = topofpage stuff (from testtopbar2div.html)
    # $VERTICALMENUBAR = verticalmenubar stuff (from testnavbar2.html)
    # $MAINBODY = mainbody stuff (from whatever the latest html file fragment is from the html_create_list)
    # $FOOTER = footer stuff
    # $BOTTOMOFPAGE = bottomof page stuff
    # this ends off the html file

    # each entry of html_create_list is:
    # [ul_class_level_in_menubar, name_in_css_file , outfile_location_rel_to_public_html , outfilename ,
    #  part_filename_plus_location , name_in_vertical_menubar_and_htmlpage_title]
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

    #try:
    if (True):
        #
        # create styles.css file
        #
        create_css_file_and_write_to_disk(html_top,html_sitedir,gitdir,html_create_list,local_compile_check,website_top,css_to_use)

        #
        # now, get the majority of html files stitched together
        #
        print("starting html creation...")
        for i in range(len(html_create_list)):
            create_html_file_and_write_to_disk(html_top, html_create_list[i], \
                full_templatedir, html_full_template, \
                titlerider, \
                website_top, \
                css_filedir, css_filename, \
                gitdir, local_compile_check)

        # we're done!
        print("done with html compilation")
        
        print("We're done! Completed writing all files successfully :)")

    #except:
    else:
        print("Error: ran into a problem and crashed!!")

# --EOF--
