require 'ue_file_utils'

include UeFileUtils

class Version
  include Mongoid::Document
  include Mongoid::Timestamps

  field :version,    :type => Integer
  field :path,       :type => String
  field :file_name,  :type => String
  field :created_by, :type => String

  embedded_in :element

  before_save do
    self.path = get_path
    self.file_name = UeFileUtils::get_element_name self.element.asset.group.project.name,
                                                   self.element.asset.group.name,
                                                   self.element.asset.name, self.element.elclass,
                                                   self.element.eltype, self.element.elname,
                                                   self.version.to_i
  end
  after_save :create_dirs

  private

  def get_path
    if self.path.nil?
      UeFileUtils::get_version_path self.element.path, self.element.elclass,
                                    self.element.eltype, self.element.elname, self.version.to_i
    else
      self.path
    end
  end

  def create_dirs
    UeFileUtils::create_dir get_path
  end
end
