-----------------------------------------------------------------------------
--  agorm_rock*
-----------------------------------------------------------------------------
local Base	=	{
	blocking			= true,
	category			= "rocks",
	damage				= 100,
	description			= "Rock",
	energy				= 0,

	flammable			= false,
	footprintX			= 2,
	footprintZ			= 2,
	height				= 16,
	hitdensity			= 0,
	metal				= 10,
	reclaimable			= true,
	autoreclaimable		= true, 	
	upright 			= false,
	world				= "All Worlds",
	customparams = { 
		author = "aGorm",
		category = "rocks",
		set = "aGorms Rocks",
		normalmaps = "yes",
		normaltex = "unittextures/rocks1n.tga",
		treeshader = "no",
		randomrotate = "true",
	}, 
}

local ferns = {}
for i = 1, 5 do 
	local name = 'agorm_rock' .. i
	local def = {}
	for k, v in pairs(Base) do
		def[k] = v
	end
	def.name = name
	def.object =  'rock' .. i .. ".s3o"
	ferns[name] = def
end


return ferns