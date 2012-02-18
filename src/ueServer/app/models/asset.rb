require 'ue_file_utils'

include UeFileUtils

class Asset
  include Mongoid::Document
  include Mongoid::Timestamps

  field :name,       :type => String
  field :asset_type, :type =>String
  field :path,       :type => String
  field :created_by, :type => String

  belongs_to :group
  has_many :elements

  before_save do
    self.path = get_path
  end
  after_save :create_dirs

  def Asset.get_asset(project, group, asset)
    g = Group.get_group(project, group)
    if g == {} || g == nil
      return {}
    else
      a = g.assets.where(:name => asset).first
      if a == nil
        return {}
      else
        return a
      end
    end
  end

  def Asset.get_assets(project, group)
    g = Group.get_group(project, group)
    if g == {} || g == nil
      return []
    else
      return g.assets
    end
  end

  private

  def get_path
    if self.path.nil?
      File.join self.group.path, UeFileUtils::asset_dirs[self.asset_type][1], self.name
    else
      self.path
    end
  end

  def create_dirs
    UeFileUtils::create_dir_tree get_path, UeFileUtils::asset_dirs[self.asset_type][0]
  end
end