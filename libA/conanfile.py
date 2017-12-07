from conans import ConanFile, tools

class SharedLib(ConanFile):
    name = "libA"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"

    generators = "visual_studio"

    repo_base_path = "file:///cygdrive/c/Users/kostja/Dev/conan-example-shared"

    def source(self):
        self.run("git clone %s" % self.repo_base_path)
        self.source_folder = "%s\\%s" % (self.source_folder, self.name)

    def build(self):
        path_to_solution = "%s\\%s\\%s.sln" % (self.repo_base_path, self.name, self.name)
        build_command = tools.build_sln_command(self.settings, path_to_solution)
        command = "%s && %s" % (tools.vcvars_command(self.settings), build_command)

    def package(self):
        self.copy("*.h", dst="include/%s" % self.name, src="%s/include/%s" % (self.name, self.name))
        self.copy("*%s.lib" % self.name, dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [self.name]
