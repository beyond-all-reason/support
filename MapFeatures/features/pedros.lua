-----------------------------------------------------------------------------
--  Beherith San Pedro - pedro*
-----------------------------------------------------------------------------
local featureDef	=	{
	blocking			= true,
	category			= "vegetation",
	damage				= 100,
	description			= "San Pedro",
	energy				= 100,
	flammable			= 0,
	footprintX			= 1,
	footprintZ			= 1,
	height				= 16,
	hitdensity			= 0,
	blocking			= true,
	metal				= 0,
	reclaimable			= true,
	autoreclaimable		= true, 	
	world				= "All Worlds",
	customparams = { 
		author = "Beherith",
		category = "Plants",
		set = "Beheriths Cacti",
		normalmaps = "yes",
		normaltex = "unittextures/pedro-normal.tga",
		treeshader = "no",
		randomrotate = "true",
	}, 
}

local pedros = {}

for i = 1, 6 do 
	local name = 'pedro' .. i
	local def = {}
	for k, v in pairs(featureDef) do
		def[k] = v
	end
	def.name = name
	def.object =  name .. ".s3o"
	pedros[name] = def
end

return pedros
