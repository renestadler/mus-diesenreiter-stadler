package at.fhooe.recyclingserver.client.entity;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ProductDto {
    private String generic_name;
    private String image_url;
    private ProductPackagingDto[] packagings;
}
