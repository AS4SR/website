# website

This is a set of scripts and .part(ial) files used to compile a working copy of the AS4SR website, available at:
http://www.ase.uc.edu/~spacerobotics/


## Usage notes for AS4SR website authors

### To add new content
Follow the below, replacing `MYCONTENT` with the base name of the page that you want to create:
1. Create a file called MYCONTENT.part at https://github.com/AS4SR/website/_template_parts
1. Add your html content to the file MYCONTENT.part
1. Edit https://github.com/AS4SR/website/create_html.py so that your full html file will be generated
    1. Add your webpage to the `html_create_list` variable, where you want it to show up in the menubar (see `MYCONTENT` versus `MYCONTENTLVL2`). This should look something like:  
    `[['','','./','custom404.html','_template_parts/custom404.part','404 Error'],`
    ` ['level1','index','','index.html','_template_parts/index.part','Home'],`
    ` ['level1','MYCONTENT','./','MYCONTENT.html','_template_parts/MYCONTENT.part','NAMEOFWEBPAGE'],`
    ` ['level1','about','','about.html','_template_parts/about.part','About'],`
    ` ['level1','resources','','resources.html','_template_parts/coming_soon.part','Resources'],`
    ` ['level2','robots','','robots.html','_template_parts/coming_soon.part','Robots'],`
    ` ['level2','archived_robots','archived/','robots.html','_template_parts/coming_soon.part','Archived Robots'],`
    ` ['level2','MYCONTENTLVL2','archived/','MYCONTENTLVL2.html','_template_parts/MYCONTENTLVL2.part','NAMEOFWEBPAGE2']`
    ` ['level1','archived','','archived.html','_template_parts/coming_soon.part','Archived Projects'],`
    ` ['level2','later','archived_projects/','later.html','_template_parts/coming_soon.part','...']]`
    Note that if you don't start your listing with a 'level1' or 'level2' then the webpage is created but it isn't added to the CSS or menubar list.
1. Add images you need to reference to `./public_html/images`
1. Add publications you need to link to to `./public_html/publications`

### To update what's on the AS4SR webserver
1. Log in to the webserver
1. Copy the `pulldown_instructions.sh` file to `/home/spacerobotics` if it isn't already there, via:  
`cd /home/spacerobotics && wget https://github.com/AS4SR/website/raw/master/pulldown_instructions.sh`
1. Run at the prompt:  
`cd /home/spacerobotics && ./pulldown_instructions.sh`
1. If you see no errors, everything should have copied just fine!
1. Check the website at http://www.ase.uc.edu/~spacerobotics/ to make sure everything looks right.

### To compile a local copy of the AS4SR webserver on your local machine for testing
1. Get a local copy of this repository, via:  
`mkdir -p /home/$USER/git_pulls && cd /home/$USER/git_pulls`  
`git clone https://github.com/AS4SR/website.git`  
`cd website`
1. Remove any previously-existing local-website compilation, via:  
`rm -rf /home/$USER/test_website/html_here/`
1. Run at the prompt:  
`./create_html.py local /home/$USER/git_pulls/website/ /home/$USER/test_website/html_here/`
1. If you see no errors, everything should have copied just fine!
1. Check the website at file:///home/$USER/test_website/html_here/ to make sure everything looks right, via:
`firefox "file:///home/$USER/test_website/html_here/" &`

## Copyright
Copyright for webpage content: University of Cincinnati, 2017-2018

Copyright for code: BSD 3-clause license, University of Cincinnati, 2017-2018  
(The code is used to generate the full html webpages from the files in the `./_templates` and `./_template_parts` directories.)
