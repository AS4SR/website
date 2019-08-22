#!/usr/bin/python
"""
Copyright 2017-2018 University of Cincinnati
All rights reserved. See LICENSE file at:
https://github.com/AS4SR/website
Additional copyright may be held by others, as reflected in the commit history.
"""

import os
import sys
import shutil

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
    # then concatenate all strings (and print string to screen, not to file "vertical_menubar.part")
    verticalmenubar_part_str = "".join(verticalmenubar_part)
    #print(verticalmenubar_part_str)
    return verticalmenubar_part_str

def create_css_file_and_write_to_disk(html_sitedir,gitdir,html_create_list,website_top,css_filename):
    print("starting CSS file creation...")

    print("creating directory (" + html_sitedir + ") that it goes within...")
    # first, try and create the directory the file's gonna reside in, in case it doesn't exist already
    try:
    #    os.mkdir(html_top + html_sitedir)
        os.makedirs(html_sitedir) # will make intermediate directories if needed
        print("directory created")
    except:
        pass
    
    # grab the other file pieces you need on this run:
    print("grabbing pieces...")
    piece = []
    
    # read in CSS file template for fill-in
    filename_temp = gitdir + "_templates/styles.css.template"
    f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
    csstemplate = str(tempholdtext)
    
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
    filecontents = csstemplate.replace( "$CSSLICLASSTAGS", "".join(piece) )
    print("file stitched!")
    
    # now, write everything to the file
    filelocation_str = html_sitedir + css_filename
    print("writing "+ filelocation_str + "...")
    f = open(filelocation_str,'w');
    f.write(filecontents); f.close();
    print(filelocation_str + " has been written")

    # we're done!
    print("done with CSS file compilation")

def filereadin_replace_returnstr(filename_temp,lineoffsetbyXspaces,replacestr,html_data):
    """
    Inputs:
        filename_temp = gitdir + "_templates/SOMETHING.part"
        lineoffsetbyXspaces is None or an integer number
        replacestr = "$NAMEOFREPLACESTR"
        html_data is current string getting stuff replaced in it (assumed None if replacestr is None)
    
    Algorithm:
        if replacestr is None (html_data assumed None), then tempholdtext (the string read in from file) is returned
        else, an updated html_data string (that had replacestr replaced with tempholdtext, with proper offsetting) is returned
    
    Usage:
        html_data = filereadin_replace_returnstr(filename_temp,lineoffsetbyXspaces,replacestr,html_data)
    """
    f = open(filename_temp,'r'); tempholdtext = f.read(); f.close();
    if (lineoffsetbyXspaces is not None) and (lineoffsetbyXspaces != 0):
        #print("did tempholdreplace!! lineoffsetbyXspaces = %d" % lineoffsetbyXspaces)
        tempholdtext = tempholdtext.replace("\n","\n"+" "*lineoffsetbyXspaces) # offset each line by X spaces from left side of html file
    if replacestr is None: # html_data should be None as well
        return tempholdtext
    else:
        return html_data.replace( replacestr, tempholdtext )

def create_html_file_and_write_to_disk(html_sitedir,html_create_list_piece,full_templatedir,html_full_template,titlerider,website_top,css_to_use,gitdir):

    [ul_class_level_in_menubar, name_in_css_file , outfile_location_rel_to_public_html , outfilename , \
        part_filename_plus_location , name_in_vertical_menubar_and_htmlpage_title] = html_create_list_piece

    print("starting work on " + html_sitedir + outfile_location_rel_to_public_html + outfilename)

    print("creating directory (" + html_sitedir + outfile_location_rel_to_public_html + ") that it goes within...")
    # first, try and create the directory the file's gonna reside in, in case it doesn't exist already
    try:
        #os.mkdir(html_sitedir + outfile_location_rel_to_public_html)
        os.makedirs(html_sitedir + outfile_location_rel_to_public_html) # will make intermediate directories if needed
        print("directory created")
    except:
        pass

    # read in html file template for fill-in
    html_data = str(filereadin_replace_returnstr(full_templatedir + html_full_template,None,None,None))
    
    # grab the other file pieces you need on this run:
    print("grabbing pieces...")
    # $PAGETITLE = title of webpage, <title>--THISHERE--</title>
    # $CSSFILE = CSS file name, href="-->THISHERE<--"
    # $BODYCLASS =  body class="-->THISHERE<--"
    # $TOPOFPAGE = topofpage stuff (from testtopbar2div.html)
    # $VERTICALMENUBAR = verticalmenubar stuff (from testnavbar2.html)
    # $MAINBODY = mainbody stuff (from whatever the latest html file fragment is from the html_create_list)
    # $FOOTER = footer stuff
    # $BOTTOMOFPAGE = bottomof page stuff
    # this ends off the html file
    html_data = html_data.replace( "$PAGETITLE", name_in_vertical_menubar_and_htmlpage_title + titlerider )
    html_data = html_data.replace( "$CSSFILE", css_to_use ) # for live website, use this
    html_data = html_data.replace( "$BODYCLASS", name_in_css_file )
    html_data = filereadin_replace_returnstr(gitdir + "_templates/topofpage.part",4,"$TOPOFPAGE",html_data)
    verticalmenubar_part_str = create_and_return_verticalmenubar(html_create_list,website_top) # already offset
    html_data = html_data.replace( "$VERTICALMENUBAR", verticalmenubar_part_str )
    if (part_filename_plus_location[0:23] == '_template_parts/people/'): # then we need to create the .part file first
        people_full_template = "_template_parts/people/people_piece.part"
        people_data = str(filereadin_replace_returnstr(gitdir + people_full_template,None,None,None))
        # then do all the replacements by pulling stuff from the .txt file (& replace in the *_piece.part file)
        partfile_data = str(filereadin_replace_returnstr(gitdir + part_filename_plus_location,None,None,None))
        partfile_data_list = partfile_data.split('\n')
        print("%r\n" % (partfile_data_list,))
        for i in range(len(partfile_data_list)):
            if ("$PIC$" == partfile_data_list[i]): # then the next line contains a pic
                people_data = people_data.replace( "$PIC$", str(partfile_data_list[i+1]))
            elif (len(partfile_data_list[i])>0) and ("$" == partfile_data_list[i][0]): # then the next lines contain contact info until hit another $ section
                holdstr = ""
                for j in range(i+1,len(partfile_data_list)):
                    if (len(partfile_data_list[j])>0) and (partfile_data_list[j][0] == "$"): # if starts with a $ then done
                        break
                    else:
                        holdstr = holdstr + partfile_data_list[j] + "\n"
                if ("$MAINCONTACT$" == partfile_data_list[i]):
                    people_data = people_data.replace( "$MAINCONTACT$", holdstr )
                elif ("$PUBLICATIONS$" == partfile_data_list[i]):
                    people_data = people_data.replace( "$PUBLICATIONS$", holdstr )
                elif ("$PROJECTS$" == partfile_data_list[i]):
                    people_data = people_data.replace( "$PROJECTS$", holdstr )
                else:
                    print("Did not find a match for %s in template" % (partfile_data_list[i],))
        # now replace the stuff in the file
        html_data = html_data.replace( "$MAINBODY", people_data )
    else: # use the pre-existing part file instead
        html_data = filereadin_replace_returnstr(gitdir + part_filename_plus_location,12,"$MAINBODY",html_data)
    html_data = filereadin_replace_returnstr(gitdir + "_templates/footer.part",8,"$FOOTER",html_data)
    html_data = html_data.replace( "$BOTTOMOFPAGE", "" ) #("testbottomofpage (placeholder text)")
    print("all pieces grabbed!")
    
    # then, stitch the file together:
    print("stitching file together...")
    # do string substitution:
    filecontents = str(html_data) # already stitched above
    print("file stitched!")

    # now, write everything to the file
    filelocation_str = html_sitedir + outfile_location_rel_to_public_html + outfilename
    print("writing "+ filelocation_str + "...")
    f = open(filelocation_str,'w');
    f.write(filecontents); f.close();
    print(filelocation_str + " has been written")

if __name__ == '__main__':
    """
    Call from the same directory via:
    1$  ./create_html.py
    --or--
    2$  ./create_html.py local
    --or--
    3$  ./create_html.py local [gitdir] [html_sitedir]
    --or--
    4$  ./create_html.py [website_top] [gitdir] [html_sitedir]
    
    The 1st ($1) is the vanilla run that is used for getting the AS4SR
    website (http://www.ase.uc.edu/~spacerobotics/) compiled using the
    pulldown_instructions.sh script.
    
    The 2nd ($2) will attempt to perform a local compile of the website in
    the local computer directory /home/spacerobotics/public_html
    as per website_top and gitdir. So, if you want this to work,
    you make have to perform the following at the command prompt first:
        sudo mkdir -p /home/spacerobotics
        sudo chown -R $USER:$USER /home/spacerobotics

    The 3rd ($3) will attempt to perform a compile of the website in a
    different location, assuming that gitdir may not be in spacerobotics
    as per the usual pulldown_instructions.sh script. Example usage:
        ./create_html.py local /home/$USER/git_pulls/website/ /home/$USER/test_website/html_here/
    This will put the files in /home/$USER/test_website/html_here/ and
    create all internal links as "file:///home/$USER/test_website/html_here/"
    Due to the way shutil.copy works, if you want this to work,
    you make have to perform the following at the command prompt first:
        rm -rf /home/$USER/test_website/html_here/
    
    The 4th ($4) will attempt to perform a compile of the website in a
    different location, assuming that gitdir may not be in spacerobotics
    as per the usual pulldown_instructions.sh script. Example usage:
        ./create_html.py https://www.spacerobotics.uc.edu/~$USER/ /home/$USER/git_pulls/website/ /home/$USER/my_website/public_html/
    This will put the files in /home/$USER/my_website/public_html/ and
    create all internal links as "https://www.spacerobotics.uc.edu/~$USER/"
    Due to the way shutil.copy works, if you want this to work,
    you make have to perform the following at the command prompt first:
        rm -rf /home/$USER/my_website/public_html
    """
    
    # ---- Parameters for html site creation ----
    website_top="http://www.ase.uc.edu/~spacerobotics/"
    # website_top will be find-replaced with gitdir if local_compile_check = "yes" below
    gitdir = "/home/spacerobotics/git_pulls/website-master/"
    html_sitedir = "/home/spacerobotics/public_html/"

    # ---- Get commandline variables (some can overwrite the above) ----
    local_compile_check = "no" # for live website # this is the default compilation option
    holdargs = sys.argv
    if len(holdargs)>1:
        if isinstance(holdargs[1],str):
            if holdargs[1] == "local": # for local compile, type "local" at the prompt
                local_compile_check = "yes" # for local directory checks of website, not-live, use this -- note that body images &etc. will not work
                website_top = "file://" + html_sitedir
            else: # is not a local compile, have other vars
                website_top = holdargs[1]
    print("*** local_compile_check = %s ***" % local_compile_check)
    if len(holdargs)>3:
        if isinstance(holdargs[2],str) and isinstance(holdargs[3],str):
            gitdir = holdargs[2]
            html_sitedir = holdargs[3]
            if (local_compile_check == "yes"): # html_sitedir is global directory
                website_top = "file://" + html_sitedir
            #else: the new website_top was given earlier
    print("*** html_sitedir = %s ***" % html_sitedir)
    print("*** website_top = %s ***" % website_top)


    # we are going to assume that the directory doesn't exist yet because it's a new wget download-and-unzip

    css_filename = "styles.css"
    #css_dir is html_sitedir
    #css_to_use = gitdir + "public_html/" + css_filedir + css_filename
    css_to_use = website_top + css_filename

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
     ['level1','publications','','publications.html','_template_parts/publications.part','Publications'],
     
     ['level1','people','','people.html','_template_parts/people.part','People'],
     #['','','people/','mcghan.html','_template_parts/people/mcghancl.part','Prof. Cat McGhan'],
     #['','','people/','verbryke.html','_template_parts/people/verbrymr.part','Matthew Verbryke'],
     #['','','people/','medhi.html','_template_parts/people/medhijk.part','Jishu Medhi'],
     #['','','people/','shi.html','_template_parts/people/shizu.part','Zhenyu Shi'],
     #['','','people/','korte.html','_template_parts/people/kortecm.part','Chris Korte'],
     ['','','people/','mcghan.html','_template_parts/people/mcghancl.txt','Prof. Cat McGhan'],
     ['','','people/','verbryke.html','_template_parts/people/verbrymr.txt','Matthew Verbryke'],
     ['','','people/','medhi.html','_template_parts/people/medhijk.txt','Jishu Medhi'],
     ['','','people/','shi.html','_template_parts/people/shizu.txt','Zhenyu Shi'],
     ['','','people/','korte.html','_template_parts/people/kortecm.txt','Chris Korte'],
     ['','','people/','muthaiah.html','_template_parts/people/muthaipd.txt','Ponaravind Muthaiah'],
     ['','','people/','karra.html','_template_parts/people/karrasa.txt','Sailendra Karra'],
     ['','','people/','kashid.html','_template_parts/people/kashidsv.txt','Sujeet Kashid'],

     ['level1','research','','research.html','_template_parts/research.part','Research'],
     ['level2','dualarm_inmoov','research/','dualarm_inmoov.html','_template_parts/research/dualarm_inmoov.part','Dual-arm Manipulation'],
     ['level2','aerialmanip','research/','aerialmanip.html','_template_parts/research/aerialmanip.part','Aerial Manipulator'],
     ['level2','vr_gazebo','research/','vrplusgazebo.html','_template_parts/research/vrplusgazebo.part','VR + ROS Gazebo'],
     ['level2','medicalmanip','research/','medicalmanip.html','_template_parts/research/medicalmanip.part','Medical Manipulator'],
     ['level2','rse_cont','research/','rse_cont.html','_template_parts/research/rse2pt0.part','Resilient Spacecraft Executive'],
     ['level2','tss_cont','research/','tss_cont.html','_template_parts/research/tss2pt0.part','Total System Stability'],

     ['level1','projects','','projects.html','_template_parts/unassigned_projects.part','Unassigned Projects'], # open projects
     
     ['level1','links','','links.html','_template_parts/links.part','Links'],
     #['level2','resources','','resources.html','_template_parts/resources.part','Resources at UC'],
     #['level2','related','','related.html','_template_parts/related_labs.part','Related Labs'],

     ['level1','robots','','robots.html','_template_parts/robots.part','Robots'],
     #['level2','','robots/','rovers.html','_template_parts/robots/rovers.part','Rovers'],
     #['level2','','robots/','uavs.html','_template_parts/robots/uavs.part','UAVs'],
     #['level2','','robots/','arms.html','_template_parts/robots/arms.part','Manipulators'],
     #['level2','','robots/','misc.html','_template_parts/robots/misc.part','Misc. Robots'],
     
     ['level1','archived','','archived.html','_template_parts/archived.part','Archived Work'],
     #['level2','archived_projects','archived_projects/','projects.html','_template_parts/archived_projects.part','Archived Projects'],
     #['level2','archived_robots','archived_robots/','robots.html','_template_parts/archived_robots.part','Archived Robots']]
     ['','','archived_projects/','projects.html','_template_parts/archived_projects.part','Archived Projects'],
     ['','','archived_robots/','robots.html','_template_parts/archived_robots.part','Archived Robots']]
    
    titlerider = " - AS4SR Lab, University of Cincinnati"

    # ---- end parameters for html site creation ----

    #try:
    if (True):
        #
        # move all stuff in current gitdir public_html directory over, just in case (for the overwrite)
        #
        print("copying contents of " + gitdir + "public_html to " + html_sitedir + " -- will fail if dir already exists...")
        try:
            shutil.copytree(gitdir + "public_html/./", html_sitedir) # copy src to dst, must not already exist
        except:
            print("directory already exists, stopping script run")
            sys.exit(1)
        
        #
        # create styles.css file
        #
        create_css_file_and_write_to_disk(html_sitedir,gitdir,html_create_list,website_top,css_filename)

        #
        # now, get the majority of html files stitched together
        #
        print("starting html creation...")
        for i in range(len(html_create_list)):
            create_html_file_and_write_to_disk(html_sitedir, html_create_list[i], \
                full_templatedir, html_full_template, \
                titlerider, \
                website_top, \
                css_to_use, \
                gitdir)

        # we're done!
        print("done with html compilation")
        
        print("We're done! Completed writing all files successfully :)")

    #except:
    else:
        print("Error: ran into a problem and crashed!!")

# --EOF--
