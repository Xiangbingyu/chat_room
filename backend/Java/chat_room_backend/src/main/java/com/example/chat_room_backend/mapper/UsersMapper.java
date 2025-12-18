package com.example.chat_room_backend.mapper;


import com.example.chat_room_backend.entity.Users;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface UsersMapper {
    /**
     * 插入新用户
     * @param user 用户对象
     * @return 影响的行数
     */
    int insert(Users user);

    /**
     * 根据用户名查询用户
     * @param username 用户名
     * @return 用户对象
     */
    Users selectByUsername(@Param("username") String username);
}