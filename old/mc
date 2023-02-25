execute as @e[tag=mv] at @e[tag=mv] unless block ~ ~ ~ minecraft:red_wool run tp ^ ^ ^-1

execute as @e[tag=mv] at @e[tag=mv] if block ~ ~ ~ minecraft:red_wool run setblock ~-1 ~ ~ minecraft:blue_wool

execute as @e[tag=mv] at @e[tag=mv] if block ~ ~ ~ minecraft:red_wool run tp ~-1 ~ ~

execute as @e[tag=mv] at @e[tag=mv] if block ~ ~ ~ minecraft:blue_wool run setblock ~-1 ~ ~ minecraft:red_wool

execute as @e[tag=mv] at @e[tag=mv] if block ~ ~ ~ minecraft:blue_wool run tp @e[tag=mv] ~ ~ ~ facing ^ ^ ^-1

execute as @e[tag=mv] at @e[tag=mv] run setblock ~ ~-1 ~ minecraft:yellow_wool

// execute as @e[tag=mv] at @e[tag=mv] unless block ~ ~1 ~ air run tp ~ ~1 ~

// execute as @e[tag=mv] at @e[tag=mv] if block ~ ~ ~ air if block ~ ~-1 ~ air run tp ~ ~-1 ~

execute at @e[tag=mv] as @e[tag=mv] unless block ~ ~ ~ minecraft:command_block unless block ~ ~ ~ minecraft:red_wool unless block ~ ~ ~ minecraft:blue_wool run setblock ~ ~ ~ air destroy