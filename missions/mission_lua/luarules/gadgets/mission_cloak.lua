function gadget:GetInfo()
    return {
        name      = 'Mission Cloaker',
        desc      = 'Exposes a function to cloak all AI units that can be cloaked',
        author    = 'Bluestone',
        version   = '',
        date      = 'August 2014',
        license   = 'GPL v3 or later',
        layer     = 0,
        enabled   = true
    }
end

-- SYNCED --
if (gadgetHandler:IsSyncedCode()) then

function CloakAIUnits()
    needUpdate = true
end

function gadget:GameFrame(n)
    if n<2 then return end --to handle update requests received  before the game starts
    
    if needUpdate then
        Update()
        needUpdate = false
    end
end

function Update()
    -- work out which are the "AI" teams in the mission
    local AITeams = {}
    local allyTeams = Spring.GetAllyTeamList()
    for _,aID in ipairs(allyTeams) do
        local teamList = Spring.GetTeamList(aID)
        for _,tID in ipairs(teamList) do
            local _, _, _, isAITeam, _, _ = Spring.GetTeamInfo(tID)
            if isAITeam then
                AITeams[#AITeams+1] = tID
            end
        end
    end
    
    for _,tID in ipairs(AITeams) do
        local units = Spring.GetTeamUnits(tID)
        for _,uID in ipairs(units) do
            Spring.GiveOrderToUnit(uID, CMD.CLOAK, {1}, {})
        end
    end
end

GG.CloakAIUnits = CloakAIUnits

-- UNSYNCED --
else
    return false
end


