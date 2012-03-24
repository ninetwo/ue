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
    self.file_name = get_name
  end
  after_save do
    UeFileUtils::create_dir get_path
  end

  before_destroy do
    UeFileUtils::delete_dir self.path
  end

  private

  def get_path
    if self.path.nil?
      UeFileUtils::get_version_path self.element.path, self.element.elclass,
                                    self.element.eltype, self.element.elname, self.version.to_i
    else
      self.path
    end
  end

  def get_name
    UeFileUtils::get_element_name self.element.asset.group.project.name,
                                  self.element.asset.group.name,
                                  self.element.asset.name, self.element.elclass,
                                  self.element.eltype,     self.element.elname,
                                  self.version.to_i
  end
end
