# Use spads_coop_instance.conf

The spads_coop_instance.conf config is the one to use for SPADS.
Remember to:
- Give it a hostid=[two digit number] parameter when launching, this specifies the account used and the ports that will be used (check the file!)
- Register lobby accounts for the lobbylogin field
- Add the password
- Create the relevant spads_host%hostid% instancedir
- Create the relevant spads_host%hostid%\log log dir

Some ramblings (Beherith) about running autohosts:
- Running autohosts by third parties is not encouraged by default. Please get in touch with developers if you want to do this. You will need to do this anyway to obtain botflags. 
- If you do, make sure you have all of the users permissions (BAR devs) set accordingly
- Please adhere to the certified/official maps list, exemption requests are welcome.
- Please try to adhere to the setup in the default spads.conf in this repo
- Attempt to use the springsettings.cfg in this repo
- Keep your hosts up to date (pr-downloader timer service, byar-maps timer service)
