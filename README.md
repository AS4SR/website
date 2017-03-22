# website

This is a working copy of the AS4SR website, available at:
http://www.ase.uc.edu/~spacerobotics/


## Usage notes for AS4SR website authors

### To add new content
Follow the below, replacing `MYCONTENT` with the base name of the page that you want to create:
1. Create a file called MYCONTENT.part at https://github.com/AS4SR/website/public_html/_template_parts
1. Add your html content to the file MYCONTENT.part
1. Edit https://github.com/AS4SR/website/public_html/_templates/verticalmenubar.part to link to your file
    1. Create a line in the menubar that links to your page. This should look something like:  
     `<li class="MYCONTENT"><a href='MYCONTENT.html'>NAMEOFWEBPAGE</a></li>`
1. Edit https://github.com/AS4SR/website/create_html.py so that your full html file will be generated
    1. Add your webpage to the `html_create_list` variable. This should look something like:  
    `['MYCONTENT','./','MYCONTENT.html','_template_parts/MYCONTENT.part','NAMEOFWEBPAGE']`
1. Edit https://github.com/AS4SR/website/public_html/styles.css so that your html file will be highlighted correctly in the menubar
    1. Create a line in the CSS stylesheet so that your page will show up red if it's the current page. This should be added around lines 161-170 to the list that's already there, and should look something like:  
    `body.MYCONTENT li.MYCONTENT a,`
1. Add images you need to reference to https://github.com/AS4SR/website/public_html/images
1. Add publications you need to link to to https://github.com/AS4SR/website/public_html/publications

### To update what's on the webserver
1. Log in to the webserver
1. Copy the `pulldown_instructions2.sh` file to `/home/spacerobotics` if it isn't already there, via:  
`cd /home/spacerobotics && wget https://github.com/AS4SR/website/raw/master/pulldown_instructions2.sh`
1. Run at the prompt:  
`cd /home/spacerobotics && ./pulldown_instructions2.sh`
1. If you see no errors, everything should have copied just fine!
1. Check the website at http://www.ase.uc.edu/~spacerobotics/ to make sure everything looks right.


## Copyright
Copyright for webpage content: University of Cincinnati, 2017

Copyright for code: BSD 3-clause license, University of Cincinnati, 2017  
(The code is used to generate the full html webpages from the files in the `public_html/_templates` and `public_html/_template_parts` directories.)
