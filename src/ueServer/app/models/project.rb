require 'ue_file_utils'

include UeFileUtils

class Project
  include Mongoid::Document
  include Mongoid::Timestamps

  field :name,       :type => String
  field :path,       :type => String
  field :created_by, :type => String

  has_many :groups

  before_save do
    self.path = get_path
  end

  after_save do
    UeFileUtils::create_dir_tree get_path, UeFileUtils::project_dirs
  end

  before_destroy do
    self.groups.destroy_all
    UeFileUtils::delete_dir self.path
  end

  def self.get_project project
    p = Project.where(:name => project).first
    if p.nil?
      return {}
    else
      return p
    end
  end

  private

  def get_path
    if self.path.nil?
      File.join "/work", self.name
    else
      self.path
    end
  end
end
