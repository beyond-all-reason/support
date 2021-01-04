-----------------------------------------------------------------------------
--  Beherith Peyote
-----------------------------------------------------------------------------
local featureDef	=	{
	blocking			= true,
	category			= "vegetation",
	damage				= 100,
	description			= "Peyote",
	energy				= 5,
	flammable			= 0,
	footprintX			= 0,
	footprintZ			= 0,
	height				= 8,
	hitdensity			= 0,
	blocking			= false,
	metal				= 0,
	reclaimable			= true,
	autoreclaimable		= true, 	
	world				= "All Worlds",	
	customparams = { 
		author = "Beherith",
		category = "Plants",
		set = "Beheriths Cacti",
		normalmaps = "yes",
		normaltex = "unittextures/peyote-normal.tga",
		treeshader = "no",
		randomrotate = "true",
	}, 
}

local peyotes = {}

for i = 1, 4 do 
	local name = 'peyote' .. i
	local def = {}
	for k, v in pairs(featureDef) do
		def[k] = v
	end
	def.name = name
	def.object =  name .. ".s3o"
	peyotes[name] = def
end

return peyotes
