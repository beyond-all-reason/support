local featureDef =	{
	--name			= "allpinesb_ad0_green_c_xl",
	world				="All Worlds",
	description			="Pine Tree",
	category			="Vegetation",
	--object			="allpinesb_ad0_green_c_xl.s3o",
	footprintx			=1,
	footprintz			=1,
	--height			=30,
	blocking			=true,
	upright				=true,
	hitdensity			=0,
	--energy 			= 100,
	metal				=0,
	--damage			= 20,
	flammable			=true,
	reclaimable			=true,
	autoreclaimable		=true,

	customparams = {
		author = "Beherith, 0 A.D.",
		category = "Plants",
		set = "Beheriths Pines",
		model_author = "Beherith",
		normalmaps = "yes",
		normaltex = "unittextures/allpinesb_ad0_normal.dds",
		lod_master = "allpinesb_ad0_green_c_xl",
		lod_level = 1,
		treeshader = "yes",
		randomrotate = "true",
	},
}

local allpinesb = {}

for _,treecolor in pairs({'green','brown','snow','snowgreen'}) do
	for _,treetype in pairs ({'a','b','c'}) do
		for sizeidx,treesize in pairs({'xs','s','m','l','xl','xxl'}) do 
			local name = 'allpinesb_ad0_' ..treecolor .. '_' .. treetype .. '_' .. treesize --allpinesb_ad0_green_c_xl
			local def = {}
			for k, v in pairs(featureDef) do
				def[k] = v
			end
			def.name = name
			def.object = name .. ".s3o"
			def.energy = sizeidx * 50
			def.height = sizeidx * 10 + 10
			def.damage = sizeidx * 20
			allpinesb[name] = def
		end
	end
end

return allpinesb


--allpinesb_ad0_green_c_xl,allpinesb_ad0_green_c_l,allpinesb_ad0_green_c_xxl,allpinesb_ad0_green_b_xl,allpinesb_ad0_green_b_l,allpinesb_ad0_green_b_xxl,allpinesb_ad0_green_a_xl,allpinesb_ad0_green_a_l,allpinesb_ad0_green_a_xxl,allpinesb_ad0_snow_b_xl,allpinesb_ad0_snow_b_l,allpinesb_ad0_snow_b_xxl,allpinesb_ad0_snow_c_xl,allpinesb_ad0_snow_c_l,allpinesb_ad0_snow_c_xxl,allpinesb_ad0_snow_a_xl,allpinesb_ad0_snow_a_l,allpinesb_ad0_snow_a_xxl,allpinesb_ad0_brown_b_xl,allpinesb_ad0_brown_b_l,allpinesb_ad0_brown_b_xxl,allpinesb_ad0_brown_c_xl,allpinesb_ad0_brown_c_l,allpinesb_ad0_brown_c_xxl,allpinesb_ad0_brown_a_xl,allpinesb_ad0_brown_a_l,allpinesb_ad0_brown_a_xxl,allpinesb_ad0_snowgreen_a_xl,allpinesb_ad0_snowgreen_a_l,allpinesb_ad0_snowgreen_a_xxl,allpinesb_ad0_snowgreen_b_xl,allpinesb_ad0_snowgreen_b_l,allpinesb_ad0_snowgreen_b_xxl,allpinesb_ad0_snowgreen_c_xl,allpinesb_ad0_snowgreen_c_l,allpinesb_ad0_snowgreen_c_xxl,allpinesb_ad0_green_c_m,allpinesb_ad0_green_c_s,allpinesb_ad0_green_c_xs,allpinesb_ad0_green_b_m,allpinesb_ad0_green_b_s,allpinesb_ad0_green_b_xs,allpinesb_ad0_green_a_m,allpinesb_ad0_green_a_s,allpinesb_ad0_green_a_xs,allpinesb_ad0_snow_b_m,allpinesb_ad0_snow_b_s,allpinesb_ad0_snow_b_xs,allpinesb_ad0_snow_c_m,allpinesb_ad0_snow_c_s,allpinesb_ad0_snow_c_xs,allpinesb_ad0_snow_a_m,allpinesb_ad0_snow_a_s,allpinesb_ad0_snow_a_xs,allpinesb_ad0_brown_b_m,allpinesb_ad0_brown_b_s,allpinesb_ad0_brown_b_xs,allpinesb_ad0_brown_c_m,allpinesb_ad0_brown_c_s,allpinesb_ad0_brown_c_xs,allpinesb_ad0_brown_a_m,allpinesb_ad0_brown_a_s,allpinesb_ad0_brown_a_xs,allpinesb_ad0_snowgreen_a_m,allpinesb_ad0_snowgreen_a_s,allpinesb_ad0_snowgreen_a_xs,allpinesb_ad0_snowgreen_b_m,allpinesb_ad0_snowgreen_b_s,allpinesb_ad0_snowgreen_b_xs,allpinesb_ad0_snowgreen_c_m,allpinesb_ad0_snowgreen_c_s,allpinesb_ad0_snowgreen_c_xs