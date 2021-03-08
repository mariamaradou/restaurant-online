DELETE FROM `project_db20_up1046879`.`Menu_item`;
DELETE FROM `project_db20_up1046879`.`Table`;
DELETE FROM `project_db20_up1046879`.`Restaurant`;

INSERT INTO `project_db20_up1046879`.`Restaurant`
(`idRestaurant`,
`name`,
`address`,
`phone`,
`username`,
`password`)
VALUES
('1','Has_nam0','Address_line 1, City0', '1234567890','res1','123'),
('2','Has_name1','Address_line 2, City1', '0123456789','res2','234');

INSERT INTO `project_db20_up1046879`.`Table`
(`idTable`,
`chairs_number`,
`Description`,
`idRestaurant`)
VALUES
('1','2','Non-smoking', '1'),
('2','4','Smoking', '1'),
('3','2','Smoking', '1'),
('4','6','Non-Smoking', '1'),
('5','2','Non-Smoking', '1'),
('6','3','Smoking','2'),
('7','4','Non-Smoking','2'),
('8','2','Non-Smoking','2')
;

INSERT INTO `project_db20_up1046879`.`Menu_item`
(`idMenu_item`,
`item_name`,
`item_price`)
VALUES
('1', 'Stake', '10'),
('2', 'Hamburger', '5'),
('3', 'Seafood', '8'),
('4', 'Water', '1'),
('5', 'Wine', '20'),
('6', 'Salad', '6'),
('7', 'Risotto', '10');






