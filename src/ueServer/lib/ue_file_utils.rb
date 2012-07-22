module UeFileUtils
  def project_dirs
    {
     "bin" => nil,
     "edt" => nil,
     "etc" => {
               "nuke" => ["template/proj/etc/nuke/*"],
               "maya" => ["template/proj/etc/maya/*"]
              },
     "lib" => nil,
     "seq" => nil,
     "tmp" => ["template/proj/tmp/*"],
     "var" => {
               "thumbs" => nil
              }
    }
  end

  def group_dirs
    {
     "default" => [{
                    },
                   "seq"],
     "lib"     => [{
                    },
                   "lib"],
     "edt"     => [{
                    },
                   ""]
    }
  end

  def asset_dirs
    {
     "default" => [{
                    "output" => nil,
                    "render" => nil,
                    "tmp"    => nil,
                    ""       => ["template/asst/workspace.mel"]
                   },
                   ""],
     "lib"     => [{
                    "tmp"    => nil,
                    ""       => ["template/asst/workspace.mel"]
                   },
                   ""],
     "edt"     => [{
                    "tmp"    => nil,
                    "edl"    => nil
                   },
                   ""]
    }
  end

  def asset_classes
    {
     "o"   => {
               "name" => "Output"
              },
     "edt" => {
               "name" => "Edit description"
              },
     "col" => {
               "name" => "Animation colour palette"
              },
     "sb"  => {
               "name" => "Storyboard"
              },
     "an"  => {
               "name" => "Animatic",
               "pathappend"  => "%%version%%"
              },
     "ns"  => {
               "name" => "Nuke script"
              },
     "nr"  => {
               "name" => "Nuke render",
               "pathprepend" => "render",
               "pathappend"  => "%%version%%"
              },
     "giz" => {
               "name" => "Nuke gizmo",
               "pathprepend" => "gizmo"
              },
     "scp" => {
               "name" => "Nuke scriptlet",
               "pathprepend" => "scriptlets"
              },
     "ms"  => {
               "name" => "Maya scene"
              },
     "mr"  => {
               "name" => "Maya render",
               "pathprepend" => "render",
               "pathappend"  => "%%version%%"
              },
     "tvp" => {
               "name" => "TVPaint document"
              },
     "cel" => {
               "name" => "Cel sequence",
               "pathprepend" => "cel",
               "pathappend"  => "%%version%%"
              },
     "ps"  => {
               "name" => "Photoshop document"
              },
     "bg"  => {
               "name" => "Background"
              },
     "ae"  => {
               "name" => "After Effects document"
              },
     "ar"  => {
               "name" => "After Effects render",
               "pathprepend" => "render",
               "pathappend"  => "%%version%%"
              },
     "geo" => {
               "name" => "Geometry"
              },
     "cam" => {
               "name" => "Camera"
              },
     "lgt" => {
               "name" => "Light"
              },
     "tex" => {
               "name" => "Texture"
              },
     "mrs" => {
               "name" => "Mental Ray shading group"
              },
     "arc" => {
               "name" => "Architect library"
              }
    }
  end

  def parse_path p, opts={}
    opts.each do |k, v|
      if k == "vers"
        p = p.sub("%%version%%", "%04d" % v)
      end
    end
    return p
  end

  def get_element_path asset_path, elclass, eltype, elname
    if asset_classes[elclass].has_key?("pathprepend")
      File.join asset_path, asset_classes[elclass]["pathprepend"], eltype, elname
    else
      File.join asset_path, eltype, elname
    end
  end

  def get_version_path element_path, elclass, eltype, elname, vers
    if asset_classes[elclass].has_key?("pathappend")
      File.join element_path, parse_path(asset_classes[elclass]["pathappend"], opts={"vers" => vers})
    else
      element_path
    end
  end

  def get_element_name proj, grp, asst, elclass, eltype, elname, vers
    "%s_%s_%s_%s_%s_%s_%04d" % [proj, grp, asst, elname, eltype, elclass, vers]
  end

  def create_dir_tree d, a
    create_dir d
    if a.is_a? Array
      a.each do |pa|
        copy_files pa, d
      end
    elsif a.is_a? Hash
      a.each do |pk, pv|
        create_dir_tree File.join(d, pk), pv
      end
    end
  end

  def create_dir d
    FileUtils.mkdir_p d
  end

  def copy_file f, d
    FileUtils.cp f, d
  end

  def copy_files f, d
    Dir.glob(File.join("/work/bin/ue", f)).each do |fi|
      copy_file(fi, d)
    end
  end

  def delete_dir d
    FileUtils.rm_rf d
  end
end
