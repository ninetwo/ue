require 'ue_file_utils'

include UeFileUtils

class Version
  include Mongoid::Document
  include Mongoid::Timestamps

  field :version,    :type => Integer
  field :path,       :type => String
  field :created_by, :type => String

  embedded_in :element

  after_save :create_dirs
  after_initialize do
    self.path = get_path
  end

  private

  def get_path
    if self.path.nil?
      UeFileUtils::get_version_path self.element.path, self.element.elclass, self.element.eltype, self.element.elname, self.version
    else
      self.path
    end
  end

  def create_dirs
    UeFileUtils::create_dir get_path
  end
end
