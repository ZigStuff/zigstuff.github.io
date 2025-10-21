# Adding C into your build.zig

So, a while back I wanted to see how easy it was to directly integrate Lua into Zig, but not just as a shared and/or static library, but my own modified version of Lua. This would work well with any kind of C without having to constantly modify build.zig every time you added a new C source file. This is for Zig 15.1, earlier versions are a little bit different, as is the ever changing ways.

```zig
    const cflags = [_][]const u8 {
        "-std=c99",
        "-Wall",
        "-Wextra",
        "-DLUA_COMPAT_5_3",
        switch(builtin.target.os.tag) {
            .linux => "-DLUA_USE_LINUX",
            .macos => "-DLUA_USE_MACOSX",
            .windows => "-DLUA_USE_POSIX",
            else => "-DLUA_USE_POSIX",
        },
    };

    // Add any C Sources in src

    var cSources = std.ArrayList([]const u8).init(b.allocator);
    var srcDir = try std.fs.cwd().openDir("src", .{.iterate = true, .access_sub_paths = true,});
    defer srcDir.close();

    var walker = try srcDir.walk(b.allocator);
    defer walker.deinit();

    while(try walker.next()) |file| {
        if(std.mem.eql(u8, std.fs.path.extension(file.basename), ".c")) {
            try cSources.append(b.pathJoin(&.{"src", file.path}));
        }
    }
    exe.addCSourceFiles(.{.files = cSources.items, .flags = &cflags,});
    
    exe.addIncludePath(b.path("include"));
    exe.addIncludePath(b.path("src/lualib"));
    exe.addLibraryPath(b.path("lib"));
```
