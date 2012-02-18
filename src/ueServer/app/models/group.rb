require 'ue_file_utils'

include UeFileUtils

class Group
  include Mongoid::Document
  include Mongoid::Timestamps

  field :name,        :type => String
  field :group_type,  :type => String
  field :path,        :type => String
  field :created_by,  :type => String

  belongs_to :project
  has_many :assets

  before_save do
    self.path = get_path
  end
  after_save :create_dirs

  def self.get_group project, group
    p = Project.get_project project
    if p == {} || p.nil?
      return {}
    else
      g = p.groups.where(:name => group).first
      if g.nil?
        return {}
      else
        return g
      end
    end
  end

  def self.get_groups project
    p = Project.get_project project
    if p == {} || p.nil?
      return []
    else
      return p.groups
    end
  end

  private

  def get_path
    if self.path.nil?
      File.join self.project.path, UeFileUtils::group_dirs[self.group_type][1], self.name
    else
      self.path
    end
  end

  def create_dirs
    UeFileUtils::create_dir_tree get_path, UeFileUtils::group_dirs[self.group_type][0]
  end
end
