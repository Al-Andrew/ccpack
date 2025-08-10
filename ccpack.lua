--[[
    CCPack Lua script for packaging a project for use with ComputerCraft

    This script is designed to be run in a ComputerCraft environment.

    Usage:
    1. wget https://raw.githubusercontent.com/Al-Andrew/ccpack/main/ccpack.lua
    2. ccpack.lua <package_you_want_installed>

    This the package name will be something like "Al-Andrew/cc-afk" (it should be hosted on GitHub)
    This script will look for a baked_manifest.json file in the root of the repository.
    If it exists, it will use that to install the package.

    The files get installed in a directory named after the package in the current working directory.
--]]


---@class BakedFile
---@field path string The path to the file relative to the package root
---@field url string The URL to download the file from

---@class BakedManifest
---@field name string The name of the package
---@field version string The version of the package
---@field url string The URL to download the package from
---@field files table<BakedFile> A list of files to download for the package


--- Does a http get on the url looking for a baked_manifest.json file
---@param package_name string The name of the package
---@return BakedManifest The parsed manifest object
local function get_manifest(package_name)
    local url = "https://raw.githubusercontent.com/" .. package_name .. "/main/baked_manifest.json" -- todo: support other branches/versions
    -- local response = http.get(url)

    -- cant use http by default, just use wget
    shell.run("wget " .. url .. " baked_manifest.json")

    if not fs.exists("baked_manifest.json") then
        error("Failed to download manifest from " .. url)
    end

    local file = fs.open("baked_manifest.json", "r")
    if not file then
        error("Failed to open manifest file: baked_manifest.json")
    end

    ---@type string
    local content = file.readAll()
    file.close()
    
    fs.delete("baked_manifest.json") -- clean up the manifest file after reading
    
    if not content or content == "" then
        error("Manifest file is empty: baked_manifest.json")
    end

    return textutils.unserializeJSON(content)
end


--- Creates a directory if it does not exist, including parent directories
--- @param path string The path to the directory to create
local function mkdir_if_not_exists_with_parent(path)
    if fs.exists(path) then
        return
    end
    
    local parent = fs.getDir(path)
    if not fs.exists(parent) then
        mkdir_if_not_exists_with_parent(parent)
    end
    fs.makeDir(path)
end

--- Downloads a file from the given URL and saves it to the specified path
---@param path string The path to save the file to
---@param url string The URL to download the file from
local function download_file_to_path(path, url)
    mkdir_if_not_exists_with_parent(fs.getDir(path))
    
    local response = http.get(url)
    if not response then
        error("Failed to download file from " .. url)
    end

    local file = fs.open(path, "wb")
    if not file then
        error("Failed to open file for writing: " .. path)
    end

    file.write(response.readAll())
    file.close()
    response.close()
end

--- Installs a package by downloading its files according to the manifest
---@param package_name string The name of the package to install
local function install_package(package_name)
    print("Installing package: " .. package_name)

    local manifest = get_manifest(package_name)
    if not manifest or not manifest.files then
        error("Invalid manifest for package: " .. package_name)
    end
    print("Got manifest!")
    print("Package name: " .. manifest.name)
    print("Package version: " .. manifest.version)
    print("Package URL: " .. manifest.url)

    -- we put the package in a directory named after the package
    local package_dir = fs.combine(fs.getDir(shell.getRunningProgram()), manifest.name)
    mkdir_if_not_exists_with_parent(package_dir)

    print("Created working directory: " .. package_dir)

    for _, file in ipairs(manifest.files) do
        print("Downloading file: " .. file.path .. " from " .. file.url)
        download_file_to_path(fs.combine(package_dir, file.path), file.url)
    end
end


--- Driver code
local package_name = arg[1]
if not package_name then
    error("Usage: ccpack.lua <package_name>")
end

install_package(package_name)