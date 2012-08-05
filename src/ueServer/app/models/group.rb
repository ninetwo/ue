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

  after_save do
    UeFileUtils::create_dir_tree get_path, UeFileUtils::group_dirs[self.group_type][0]
  end

  before_destroy do
    self.assets.destroy_all
    UeFileUtils::delete_dir self.path
  end

  def self.get_group project, group
    p = Project.where(:name => project).first
    if p == {} || p.nil?
      {}
    else
      g = p.groups.where(:name => group).first
      if g.nil?
        {}
      else
        JSON.parse(p.to_json).to_hash.merge(JSON.parse(g.to_json).to_hash)
      end
    end
  end

  def self.get_groups project
    p = Project.where(:name => project).first
    if p == {} || p.nil?
      []
    else
      p.groups
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
end
