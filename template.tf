resource "alicloud_ots_instance" "my-instance" {
  name = "my-instance"
  description = "My first Table Store instance"
  accessed_by = "Any"
  instance_type = "Capacity"
}

resource "alicloud_ots_table" "table" {
  instance_name = "${alicloud_ots_instance.my-instance.name}"
  table_name = "Profile"
  primary_key = [
    {
      name = "userId"
      type = "String"
    }
  ]
  time_to_live = "-1"
  max_version = "3"
}
