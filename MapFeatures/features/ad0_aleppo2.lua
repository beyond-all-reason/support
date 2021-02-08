-----------------------------------------------------------------------------
--  Aleppo pine trees - ad0_aleppo2_*
-----------------------------------------------------------------------------
-- size ranges: s-m-l-xl -- 64 - 96 - 140 - 180 elmo trunk heights 
-- color variants dark-med-light-dead  
-- geometry variants: singleleaf, doubleleaf, doubletrunk
-- naming scheme: ad0_aleppo2_[sparse|dense|double]_[dark|med|light|dead]_[s|m|l|xl]
-- License: CC BY SA NC 3.0 @ Beherith (mysterme@gmail.com)

local featureDef	=	{
	world				="All Worlds",
	blocking			=true,
	category			="Vegetation",
	description			="Aleppo Pine",
	footprintx			=1,
	footprintz			=1,
	height				=30,
	hitdensity			=0,
	metal				=0,
	flammable			=true,
	reclaimable			=true,
	autoreclaimable		=true,
	upright				=false,
	collisionvolumetype = "box",
	collisionvolumescales = "8 64 8",
	collisionvolumeoffsets = "0 16 0",
	customparams = {
		model_author = "Beherith, 0 A.D.",
		normalmaps = "yes",
		normaltex = "unittextures/ad0_aleppo2_normal.dds",
		treeshader = "yes",
		randomrotate = "true",
		category = "Plants",
		set = "Aleppo Pine Trees",
	},
} 

local aleppopines = {}

for _,dense in ipairs({"sparse","dense","double"}) do 
	for _,color in ipairs({"dark","med","light","dead"}) do 
		for SCALEFACTOR,scale in ipairs({"s","m","l","xl"}) do 
			local name = 'ad0_aleppo2_' .. dense .. "_" .. color .. "_" .. scale
			local def = {}
			for k, v in pairs(featureDef) do
				def[k] = v
			end
			def.name = name
			def.object =  name .. ".s3o"
			def.collisionvolumescales = tostring(6*SCALEFACTOR) .. " " .. tostring(64*SCALEFACTOR) .. " " .. tostring(6*SCALEFACTOR)
			def.energy = 200*SCALEFACTOR
			def.mass = 20*SCALEFACTOR
			def.maxdamage = 500*SCALEFACTOR
			
			aleppopines[name] = def
		end
	end
end

return aleppopines
