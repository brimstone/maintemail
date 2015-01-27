#!/bin/bash -x
./maintemail.py --ics https://www.google.com/calendar/ical/uq2m73m8lvm2hf86nbfl9g8gkk%40group.calendar.google.com/private-12556f00fa50f0f4a10c2dcf65d7771f/basic.ics \
	--smtp mail.in.the.narro.ws \
	--template maint.html \
    --from maint@the.narro.ws \
	-v
