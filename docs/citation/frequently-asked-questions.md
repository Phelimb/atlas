---
title: "Frequently Asked Questions"
excerpt: ""
---
## mccortex fails to make. 

Likely problem: Submodules have not been pulled with the repo. 

Solution : Run 
	
	git pull && git submodule update --init --recursive
	cd mccortex && make