-----------------------------------------------------------------------------
--  Senegal palm trees - ad0_senegal_*
-----------------------------------------------------------------------------

local featureDef	=	{
	--name				= "ad0_senegal_1",
	world				="All Worlds",
	--object			="ad0_senegal_1.s3o",
	blocking			=true,
	category			="Vegetation",
	description			="Palm Tree",
	energy				=250,
	footprintx			=1,
	footprintz			=1,
	height				=30,
	hitdensity			=0,
	metal				=0,
	mass				=20,
	flammable			=true,
	reclaimable			=true,
	autoreclaimable		=true,
	upright				=false,
	customparams = {
		model_author = "Beherith, 0 A.D.",
		normalmaps = "yes",
		normaltex = "unittextures/ad0senegal_normal.tga",
		treeshader = "yes",
		randomrotate = "true",
		category = "Plants",
		set = "Senegal Palm Trees 0AD",
	},
} 

local senegalpalms = {}
for i = 1, 7 do 
	for _,sizeclass in pairs({'','_large'}) do
		local name = 'ad0_senegal_' .. i .. sizeclass
		local def = {}
		for k, v in pairs(featureDef) do
			def[k] = v
		end
		def.name = name
		def.object =  name .. ".s3o"
		senegalpalms[name] = def
	end
end

return senegalpalms
